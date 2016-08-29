REMOTE_DB = 'chai'

class RemoteRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == REMOTE_DB:
            return REMOTE_DB
        return None

    def db_for_write(selfself, model, **hints):
        if model._meta.app_label == REMOTE_DB:
            return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == REMOTE_DB or obj2._meta.app_label == REMOTE_DB:
            return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == REMOTE_DB:
            return False
        return True
