"""
    Import needed things
"""
from django.contrib.postgres.fields import JSONField
from django.db import models
from domain.models import TimeStampModel, Domain


class PageSeedInsight(TimeStampModel):
    """
       model for PageSeedInsight
    """
    url = models.CharField(max_length=1024)
    domain = models.CharField(max_length=1024)
    result = JSONField()
    cron_flag = models.BooleanField(default=False)
    domain_fk = models.ForeignKey(Domain, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.url)
