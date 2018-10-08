from django.contrib.admin.options import InlineModelAdmin
from .base import AdminLinkBase


class BaseInlineModelAdmin(AdminLinkBase, InlineModelAdmin):
    pass


class StackedInline(BaseInlineModelAdmin):
    template = 'admin/edit_inline/stacked.html'


class TabularInline(BaseInlineModelAdmin):
    template = 'admin/edit_inline/tabular.html'
