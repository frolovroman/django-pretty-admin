VERSION = (0, 0, 1, 'final', 0)

__title__ = 'django-pretty-admin'
__version_info__ = VERSION
__version__ = '.'.join(map(str, VERSION[:3])) + ('-{}{}'.format(
    VERSION[3], VERSION[4] or '') if VERSION[3] != 'final' else '')
__author__ = 'Roman Frolov'
