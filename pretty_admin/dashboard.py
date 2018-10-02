from __future__ import absolute_import, unicode_literals

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from django.contrib.auth import get_user_model
from django.core.exceptions import FieldDoesNotExist
from django.contrib.admin.utils import display_for_value
from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard

from .admin import AdminLinkBase
User = get_user_model()


class TableModule(modules.DashboardModule):
    template = 'admin/dashboard/table_module.html'
    check_permissions = lambda request: True
    title = None

    def __init__(self, table_data, title=None, check_permissions=None, **kwargs):
        if not self.validate_table_data(table_data):
            raise ValueError('Invalid table_data')
        self.table_data = table_data
        if check_permissions:
            self.check_permissions = check_permissions
        self.title = title
        super(TableModule, self).__init__(title, **kwargs)

    def is_permitted(self, request):
        return self.check_permissions(request)

    @staticmethod
    def validate_table_data(table_data):
        if len(table_data) < 2:
            return False
        head = table_data[0]
        for line in table_data[1:]:
            if len(line) != len(head):
                return False
        return True

    def init_with_context(self, context):
        if self._initialized or not self.is_permitted(context['request']):
            return

        head = self.table_data[0]
        self.children.append(head)

        for line in self.table_data[1:]:
            display_line = []
            for value in line:
                display_line.append(display_for_value(value, '-', isinstance(value, bool)))

            self.children.append(display_line)
        self._initialized = True


class InstanceList(AdminLinkBase, modules.DashboardModule):
    template = 'admin/dashboard/instance_list.html'
    model = None
    title = None
    queryset = None
    fields = ['pk', '__str__']
    display_links = ()

    def __init__(self, model, fields=None, title=None, queryset=None, limit=10,
                 ordering=None, display_links=None, **kwargs):
        self.model = model

        if not title:
            title = _("Last {limit} {name}").format(limit=limit, name=self.model._meta.verbose_name_plural.title())
        self.title = title

        self.queryset = self.get_queryset(queryset=queryset, limit=limit, ordering=ordering)

        if fields:
            self.fields = fields
        if not display_links:
            display_links = self.fields
        self.display_links = display_links

        super(InstanceList, self).__init__(title, **kwargs)

    def get_queryset(self, queryset=None, limit=10, ordering=None):
        queryset = queryset or self.model.objects.all()
        if ordering:
            queryset = queryset.order_by(*ordering)
        return queryset[:limit]

    def check_permissions(self, request):
        if not request.user:
            return False
        if not request.user.is_authenticated:
            return False
        return request.user.has_module_perms(self.model._meta.app_label)

    def init_with_context(self, context):
        if self._initialized or \
                not self.check_permissions(context['request']) or \
                not self.queryset.exists():
            return

        head = [self.get_display_model_field(self.model, field) for field in self.fields]
        self.children.append(head)

        for instance in self.queryset:
            instance_data = []
            for field in self.fields:
                value = self.get_display_value(instance, field)
                if field in self.display_links:
                    field_data = {'allow_tags': True,
                                  'value': u"<a href='{}'>{}</a>".format(self.admin_edit_url(instance), value)}
                else:
                    field_data = {'allow_tags': True, 'value': value}
                instance_data.append(field_data)
            self.children.append(instance_data)
        self._initialized = True

    @staticmethod
    def get_display_model_field(model, field):
        if '' in field.split("__"):
            return field.replace('__', '')
        final_field = field.split("__")[-1]
        for related_model_name in field.split("__")[:-1]:
            try:
                model = model._meta.get_field(related_model_name).rel.to
            except FieldDoesNotExist:
                pass
        try:
            return model._meta.get_field(final_field).verbose_name
        except FieldDoesNotExist:
            return final_field.replace("_", " ")

    @staticmethod
    def _parse_related_value(instance, field):
        value = None
        final_field = field.split("__")[-1]

        for related_value in field.split("__")[:-1]:
            instance = getattr(instance, related_value, None)
        if instance:
            if hasattr(instance, "get_{}_display".format(final_field)):
                value = getattr(instance, "get_{}_display".format(final_field))()
            else:
                value = getattr(instance, final_field, None)
        return value

    def get_display_value(self, instance, field):
        if '' in field.split("__"):
            value = getattr(instance, field, None)
        else:
            value = self._parse_related_value(instance, field)
        if callable(value):
            return value()
        return display_for_value(value, '-', isinstance(value, bool))


class PrettyIndexDashboard(Dashboard):
    columns = 2

    def init_with_context(self, context):

        self.children.append(modules.Group(
            title=_('Manage Data'),
            display="tabs",
            children=[
                modules.AppList(
                    _('Applications'),
                    exclude=('django.contrib.*',),
                ),
                modules.AppList(
                    _('Administration'),
                    models=('django.contrib.*',),
                ),
            ]
        ))
        self.children.append(modules.Group(
            title=_('Statistics'),
            display="tabs",
            children=[InstanceList(User)]))


class PrettyAppIndexDashboard(AppIndexDashboard):
    columns = 2

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]
