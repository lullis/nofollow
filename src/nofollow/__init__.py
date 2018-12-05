from .celery import app as celery_app

__all__ = ('celery_app',)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
