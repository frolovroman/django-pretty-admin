from django.contrib import admin
from django.contrib.admin.filters import AllValuesFieldListFilter, RelatedFieldListFilter, \
    ChoicesFieldListFilter
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseBase


class DropdownFilter(AllValuesFieldListFilter):
    template = 'admin/dropdown_filter.html'


class ChoiceDropdownFilter(ChoicesFieldListFilter):
    template = 'admin/dropdown_filter.html'


class RelatedDropdownFilter(RelatedFieldListFilter):
    template = 'admin/dropdown_filter.html'


class AdminModelExtraTable(object):
    title = None
    head = []
    body = []
    model = None
    queryset = None
    ordering = ()
    limit = None
    fields = ()
    template = 'admin/extra_table.html'

    def __init__(self):
        self.queryset = self.get_queryset()
        self.fields = self.get_fields()
        if self.title is None:
            self.title = self.model._meta.verbose_name_plural or str(self.model)
        self.head = self.get_head()
        self.body = self.get_body()
        super(AdminModelExtraTable, self).__init__()

    def get_fields(self):
        if not self.fields:
            self.fields = (str(field.name) for field in self.model._meta.get_fields())
        return self.fields

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.all()
        if self.ordering:
            self.queryset = self.queryset.order_by(*self.ordering)
        if self.limit:
            self.queryset = self.queryset[:self.limit]
        return self.queryset

    def get_head(self):
        head = []
        for field in self.fields:
            if hasattr(self, field):
                field_method = getattr(self, field)
                title = getattr(field_method, 'short_description', str(field))
            else:
                f = self.model._meta.get_field(field)
                title = f.verbose_name or f.name
            head.append(title)
        return head

    def get_body(self):
        body = []
        for obj in self.queryset:
            body.append([self.get_field_value(field, obj) for field in self.fields])
        return body

    def get_field_value(self, field, obj):
        allow_tags = False
        if hasattr(self, field):
            field_method = getattr(self, field)
            allow_tags = getattr(field_method, 'allow_tags', False)
            try:
                value = field_method(obj)
            except:
                value = '-'
        else:
            display_method_name = "get_{}_display".format(field)
            if hasattr(obj, display_method_name):
                value = getattr(obj, display_method_name)()
            else:
                value = getattr(obj, field)

        return value, allow_tags


class AdminRelatedModelExtraTable(AdminModelExtraTable):
    obj = None
    model = None
    related_field = ''
    one_to_one = False
    limit = 100

    def __init__(self, obj):
        self.obj = obj
        if not self.related_field:
            for field in obj._meta.related_objects:
                self.one_to_one = field.one_to_one
                if self.model == field.related_model:
                    self.related_field = field.related_name

        if not self.related_field:
            raise ValueError(u"{} has no relations with model {}".format(obj.__class__.__name__, self.model.__name__))

        super(AdminRelatedModelExtraTable, self).__init__()

    def get_queryset(self):
        try:
            related = getattr(self.obj, self.related_field)
            if self.one_to_one:
                return self.model.objects.filter(id=related.id)
            self.queryset = related.all()
            return super(AdminRelatedModelExtraTable, self).get_queryset()
        except:
            return self.model.objects.none()


class BaseModelAdmin(admin.ModelAdmin):
    save_on_bottom = True
    change_view_actions = []
    related_models_links = []
    change_form_extra_tables = []

    class Media:
        js = ('js/svg.js', )

    def __init__(self, model, admin_site):
        self.set_related_models_links(model)
        self.save_on_bottom = not self.save_on_top
        super(BaseModelAdmin, self).__init__(model, admin_site)

    def get_extra_tables(self, obj=None):
        extra_tables = []
        if obj:
            for extra_table in self.change_form_extra_tables:
                if issubclass(extra_table, AdminRelatedModelExtraTable):
                    extra_table_instance = extra_table(obj=obj)
                else:
                    extra_table_instance = extra_table()
                extra_tables.append(extra_table_instance)
        return extra_tables

    def get_readonly_fields(self, request, obj=None):
        fields = super(BaseModelAdmin, self).get_readonly_fields(request, obj)
        fields = list(set(list(fields) + ["{}_link".format(str(field_name))
                                          for field_name in self.related_models_links]))
        return fields

    def set_related_models_links(self, model):
        for field_name in self.related_models_links:
            field = model._meta.get_field(field_name)

            method = self.get_related_model_edit_link(field_name, field)
            method.short_description = field.verbose_name or field.name
            method.allow_tags = True
            setattr(self, method.__name__, method)

    def get_related_model_edit_link(self, field_name, field):
        def get_link(obj):
            instance = getattr(obj, field_name)
            if instance:
                name = str(instance)
                return instance.admin_edit_link(name)
            return '-'

        method = get_link
        method.__name__ = "{}_link".format(str(field_name))
        return method

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        change_view_actions_choices = [choice for choice in self.get_action_choices(request, [])
                                       if choice[0] in self.change_view_actions]
        context.update({'save_on_bottom': self.save_on_bottom,
                        'change_view_actions_choices': change_view_actions_choices,
                        "extra_tables": self.get_extra_tables(obj)})
        return super(BaseModelAdmin, self).render_change_form(request, context, add=False, change=False, form_url='', obj=None)

    def response_post_save_change(self, request, obj):
        if '_make_action' in request.POST:
            action = request.POST.get('action')
            if not action:
                return HttpResponseRedirect(request.get_full_path())
            func = self.get_actions(request)[action][0]
            queryset = self.model.objects.filter(id=obj.id)

            response = func(self, request, queryset)

            if isinstance(response, HttpResponseBase):
                return response
            else:
                return HttpResponseRedirect(request.get_full_path())

        return super(BaseModelAdmin, self).response_post_save_change(request, obj)
