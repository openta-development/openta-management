from django.conf import settings
import logging

logger = logging.getLogger(__name__)


# in the main opentasite 
# change opentasites in settings.py
# reinitialize database opentasites
# migrate opentasites


default_models = ['accounts']
site_models = ['opentasites']

class AuthRouter:
    """A router to control all database cache operations; see CacheRouter in djangoproject """

    def db_for_read(self, model, **hints):
        "All cache read operations go to the replica"
        if model._meta.app_label in site_models :
            return 'opentasites'
        else:
            return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in site_models :
            return 'opentasites'
        else :
            return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        "Only install the cache model on primary"
        return True
        if app_label == 'opentasites':
            return False
        return True

    def allow_relation( self, bj1, obj2 , **hints):
        return True
