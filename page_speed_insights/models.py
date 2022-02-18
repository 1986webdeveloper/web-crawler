from django.db import models
from domain.models import TimeStampModel
from django.contrib.postgres.fields import JSONField


# Create your models here.


class PageSeedInsight(TimeStampModel):
    url = models.CharField(max_length=1024)
    domain = models.CharField(max_length=1024)
    result = JSONField()

    def __str__(self):
        return self.url

