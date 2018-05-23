from django.contrib import admin
from django.utils.timezone import now
from django.contrib import messages
from pretty_admin.admin import DropdownFilter, RelatedDropdownFilter, AdminRelatedModelExtraTable, BaseModelAdmin

from .models import RelatedModel, MyModel


class RelatedExtraTable(AdminRelatedModelExtraTable):
    model = RelatedModel
    title = 'Related'
    fields = ('admin_edit', 'title')


@admin.register(MyModel)
class MyModelAdmin(BaseModelAdmin):
    save_on_top = True
    list_display = ('id', 'title', 'status_display', 'datetime', 'link')
    search_fields = ('title', 'status')
    change_form_extra_tables = [RelatedExtraTable, ]
    list_display_links = list_display
    list_filter = [
        ('status', DropdownFilter),
    ]
    actions = ['update_datetime', ]
    change_view_actions = ['update_datetime', ]

    def update_datetime(self, request, queryset):
        queryset.update(datetime=now())
        messages.add_message(request, messages.INFO, 'Datetime updated')

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = 'Status'

    def link(self, obj):
        return self.external_link(obj.external_url, 'External')
    link.short_description = 'Link'
    link.allow_tags = True


@admin.register(RelatedModel)
class RelatedAdmin(BaseModelAdmin):
    save_on_top = False
    list_display = ['id', 'title', 'parent', 'datetime']
    related_models_links = ['parent', ]
    list_display_links = list_display
    field = ['parent', 'title']
    search_fields = ('title', 'parent__title')
    list_filter = [
        ('parent', RelatedDropdownFilter),
        ('title', DropdownFilter),
    ]

    def datetime(self, obj):
        return obj.parent.datetime
