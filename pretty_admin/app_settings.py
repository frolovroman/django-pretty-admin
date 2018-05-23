from __future__ import absolute_import, unicode_literals
from django.conf import settings

INDEX_DASHBOARD_KEY = 'ADMIN_TOOLS_INDEX_DASHBOARD'
INDEX_DASHBOARD_DEFAULT = 'pretty_admin.dashboard.PrettyIndexDashboard'
ADMIN_TOOLS_INDEX_DASHBOARD = getattr(settings, INDEX_DASHBOARD_KEY, INDEX_DASHBOARD_DEFAULT)

APP_INDEX_DASHBOARD_KEY = 'ADMIN_TOOLS_APP_INDEX_DASHBOARD'
APP_INDEX_DASHBOARD_DEFAULT = 'pretty_admin.dashboard.PrettyAppIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = getattr(settings, APP_INDEX_DASHBOARD_KEY, APP_INDEX_DASHBOARD_DEFAULT)

THEMING_CSS_KEY = 'ADMIN_TOOLS_THEMING_CSS'
THEMING_CSS_DEFAULT = 'pretty_admin/css/admin_theming.css'
ADMIN_TOOLS_THEMING_CSS = getattr(settings, THEMING_CSS_KEY, THEMING_CSS_DEFAULT)


def patch_project_settings():
    setattr(settings, INDEX_DASHBOARD_KEY, ADMIN_TOOLS_INDEX_DASHBOARD)
    setattr(settings, APP_INDEX_DASHBOARD_KEY, ADMIN_TOOLS_APP_INDEX_DASHBOARD)
    setattr(settings, THEMING_CSS_KEY, ADMIN_TOOLS_THEMING_CSS)

    installed_apps = getattr(settings, 'INSTALLED_APPS', [])
    admin_tools_apps = ['admin_tools.theming', 'admin_tools.menu', 'admin_tools.dashboard', 'admin_tools']
    for admin_app in admin_tools_apps:
        if not admin_app in installed_apps:
            installed_apps = [admin_app, ] + installed_apps


