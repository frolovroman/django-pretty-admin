from pretty_admin.admin import AdminLinkBase
from inspect import signature


class AdminModelExtraTable(AdminLinkBase):
    title = None
    head = []
    body = []
    model = None
    queryset = None
    ordering = ()
    limit = None
    fields = ('admin_edit', '__str__')
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

    def get_overridden_method(self, field):
        if hasattr(self, field):
            field_method = getattr(self, field)
            if not callable(field_method):
                return None
            sig = signature(field_method)
            if not sig or len(sig.parameters) != 1:
                return None
            return field_method
        return None

    def get_head(self):
        head = []
        for field in self.fields:
            field_method = self.get_overridden_method(field)
            if field_method:
                title = getattr(field_method, 'short_description', str(field))
            else:
                try:
                    f = self.model._meta.get_field(field)
                    title = f.verbose_name or f.name
                except:
                    title = field
            head.append(title)
        return head

    def get_body(self):
        body = []
        for obj in self.queryset:
            body.append([self.get_field_value(field, obj) for field in self.fields])
        return body

    def get_field_value(self, field, obj):
        allow_tags = False
        field_method = self.get_overridden_method(field)
        if field_method:
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
        if callable(value):
            value = value()

        return value, allow_tags

    def admin_edit(self, obj):
        return self.admin_edit_link(obj, obj.id)
    admin_edit.short_description = 'Admin Edit'
    admin_edit.allow_tags = True


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