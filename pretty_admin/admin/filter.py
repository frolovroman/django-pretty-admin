from django.contrib.admin.filters import AllValuesFieldListFilter, RelatedFieldListFilter, \
    ChoicesFieldListFilter, BooleanFieldListFilter


class DropdownFilter(AllValuesFieldListFilter):
    template = 'admin/dropdown_filter.html'


class ChoiceDropdownFilter(ChoicesFieldListFilter):
    template = 'admin/dropdown_filter.html'


class RelatedDropdownFilter(RelatedFieldListFilter):
    template = 'admin/dropdown_filter.html'


class BooleanFieldListDropdownFilter(BooleanFieldListFilter):
    template = 'admin/dropdown_filter.html'
