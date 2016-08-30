from django.db import models


class SyncRecord(models.Model):
    last_sync_time = models.DateTimeField()
