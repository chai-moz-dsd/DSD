LOCAL_DB = 'default'

class LocalRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == LOCAL_DB:
            return LOCAL_DB
        return None

    def db_for_write(selfself, model, **hints):
        return LOCAL_DB

    def allow_relation(self, obj1, obj2, **hints):
        return LOCAL_DB

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
