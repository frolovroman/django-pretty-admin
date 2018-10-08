from django import forms
from django.contrib import admin

from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db import models

from django.http import HttpResponseRedirect
from django.http.response import HttpResponseBase

from django.utils.translation import ugettext_lazy as _


class AdminLinkBase(object):

    @staticmethod
    def external_link(url, text, target='_blank'):
        link = "<a target='{target}' class='external_link' href='{url}'>" \
               "<img src='/static/pretty_admin/img/external-link.svg' class='svg external_link'></img> " \
               "{text} </a>" \
            .format(url=url, text=text, target=target)
        return mark_safe(link)

    @staticmethod
    def internal_link(url, text, target='_self'):
        link = "<a target='{target}' class='internal_link' href='{url}'>" \
               "<img src='/static/pretty_admin/img/internal-link.svg' class='svg internal_link'></img> " \
               "{text} </a>" \
            .format(url=url, text=text, target=target)
        return mark_safe(link)

    @staticmethod
    def admin_edit_url(instance):
        return reverse("admin:%s_%s_change" %
                       (instance._meta.app_label, instance._meta.model_name), args=(instance.pk,))

    def admin_edit_link(self, instance, url_text="Edit"):
        return self.internal_link(self.admin_edit_url(instance), url_text)


class BaseModelAdmin(AdminLinkBase, admin.ModelAdmin):
    save_on_bottom = True
    change_view_actions = []
    related_models_links = []
    change_form_extra_tables = []

    formfield_overrides = {
        models.BooleanField: {'widget': forms.Select(choices=[(True, _('Yes')),
                                                              (False, _('No'))])},
        models.NullBooleanField: {'widget': forms.Select(choices=[(True, _('Yes')),
                                                                  (False, _('No')),
                                                                  (None, _('-----'))])}
    }

    class Media:
        js = ('pretty_admin/js/svg.js', )

    def __init__(self, model, admin_site):
        self.set_related_models_links(model)
        if not self.save_on_bottom and not self.save_on_top:
            self.save_on_bottom = True
        super(BaseModelAdmin, self).__init__(model, admin_site)

    def get_extra_tables(self, obj=None):
        from .extra_table import AdminRelatedModelExtraTable
        extra_tables = []
        if obj:
            for extra_table in self.change_form_extra_tables:
                if issubclass(extra_table, AdminRelatedModelExtraTable):
                    extra_tables.append(extra_table(obj=obj))
                else:
                    extra_tables.append(extra_table())
        return extra_tables

    def get_readonly_fields(self, request, obj=None):
        fields = super(BaseModelAdmin, self).get_readonly_fields(request, obj)
        fields = tuple(set(list(fields) + ["{}_link".format(str(field_name))
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
                return self.admin_edit_link(instance, str(instance))
            return '-'

        method = get_link
        method.__name__ = "{}_link".format(str(field_name))
        return method

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        change_view_actions_choices = [choice for choice in self.get_action_choices(request, [])
                                       if choice[0] in self.change_view_actions]
        context.update({
            'save_on_bottom': self.save_on_bottom,
            'change_view_actions_choices': change_view_actions_choices,
            "extra_tables": self.get_extra_tables(obj)})
        return super().render_change_form(request, context, add, change, form_url, obj)

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
