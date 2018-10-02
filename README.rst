=====
Django Pretty Admin
=====

It's just like django admin but prettier.

Fully based on `Django Admin Tools <https://github.com/django-admin-tools/django-admin-tools/>`_

Installation
-----------
1. pip install git+https://github.com/frolovroman/django-pretty-admin
2. Add pretty_admin and admin_tools to your INSTALLED_APPS setting. Put the admin_tools modules before the django.contrib.admin module!::

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


3. Add django-admin-tools to your urls.py file::

    urlpatterns = patterns('',
        url(r'^admin_tools/', include('admin_tools.urls')),
        #...other url patterns...
    )


4. Include django.contrib.staticfiles.finders.AppDirectoriesFinder into in your STATICFILES_FINDERS
5. Confing TEMPLATES:

* Include pretty_admin/templates/ into DIRS

* Set APP_DIRS=False

* Add 'admin_tools.template_loaders.Loader' to loaders

6. In the end of the settings.py add::

    from pretty_admin.app_settings import *


Examples
-----------

Try demo::


    cd demo
    pip3 install git+https://github.com/frolovroman/django-pretty-admin
    python manage.py migrate
    python manage.py loaddata fixtyres/dump.jspm
    python manage.py runserver
