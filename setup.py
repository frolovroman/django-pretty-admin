import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-pretty-admin',
    version='0.0.3',
    packages=find_packages(exclude=('demo', )),
    install_requires=[
        "django-admin-tools==0.8.1",
        "Django>=1.11",
    ],
    include_package_data=True,
    license='BSD License',
    description="It's just like django admin but prettier",
    long_description=README,
    url='https://github.com/frolovroman/django-pretty-admin',
    author='Roman Frolov',
    author_email='frolowroman@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
