from django.db import models


class Attribute(models.Model):
    class Meta:
        app_label = 'dsd'
        db_table = 'attributes'

    uid = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    valueType = models.CharField(max_length=255)
    orgUnitAttr = models.BooleanField(default=True)

    def get_attributes_as_dict(self):
        return self.convert_attributes()