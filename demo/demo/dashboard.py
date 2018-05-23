from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules
from pretty_admin.dashboard import PrettyIndexDashboard, InstanceList

from myapp.models import MyModel, RelatedModel


class MyIndexDashboard(PrettyIndexDashboard):

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
            children=[
                InstanceList(MyModel, fields=['id', 'title', 'datetime'],
                             ordering=('-status', )),
                InstanceList(RelatedModel, ordering=('-parent__status',)),
            ]
        ))
