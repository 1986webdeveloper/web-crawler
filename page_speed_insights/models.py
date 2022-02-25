"""
    Import needed things
"""
from django.contrib.postgres.fields import JSONField
from django.db import models
from domain.models import TimeStampModel


class PageSeedInsight(TimeStampModel):
    """
       model for PageSeedInsight
    """
    objects = None
    url = models.CharField(max_length=1024)
    domain = models.CharField(max_length=1024)
    result = JSONField()
    cron_flag = models.BooleanField(default=False)

    def __str__(self):
        return str(self.url)
