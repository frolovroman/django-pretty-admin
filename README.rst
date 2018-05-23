=====
Django Pretty Admin
=====

It's just like django admin but prettier.

Fully based on `Django Admin Tools <https://github.com/django-admin-tools/django-admin-tools/>`_

Installation
-----------

Add Pretty admin and admin_tools to your INSTALLED_APPS setting::

    INSTALLED_APPS = (
        'admin_tools',
        'admin_tools.theming',
        'admin_tools.menu',
        'admin_tools.dashboard',
        'pretty_admin',
        'django.contrib.auth',
        'django.contrib.sites',
        'django.contrib.admin'
        # ...other installed applications...
    )

Put the admin_tools modules before the django.contrib.admin module!
2. Add django-admin-tools to your urls.py file::

    urlpatterns = patterns('',
        url(r'^admin_tools/', include('admin_tools.urls')),
        #...other url patterns...
    )


3. Include django.contrib.staticfiles.finders.AppDirectoriesFinder into in your STATICFILES_FINDERS
4. Confing TEMPLATES:

    Include pretty_admin/templates/ into DIRS

    Set APP_DIRS=False

    Add 'admin_tools.template_loaders.Loader' to loaders
5. In the end of the settings.py add::

    from pretty_admin.app_settings import *


Examples
-----------

Try demo::


    cd demo
    pip3 install git+https://github.com/frolovroman/django-pretty-admin
    python manage.py migrate
    python manage.py loaddata fixtyres/dump.jspm
    python manage.py runserver
