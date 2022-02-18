from django.db import models
from django.contrib.auth.models import User


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Domain(TimeStampModel):
    name = models.URLField()
    user = models.ForeignKey(User, related_name="domains",
                             on_delete=models.CASCADE)
    is_fetched = models.BooleanField(default=False)

    class Meta:
        unique_together = ("name", "user",)

    def __str__(self):
        return self.name

    @property
    def status(self):
        return "FETCHING URL"


class DomainUrl(TimeStampModel):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    url = models.CharField(max_length=1024)

    class Meta:
        unique_together = ("domain", "url")


class Url(TimeStampModel):
    url = models.CharField(max_length=1024)
    domain = models.CharField(max_length=255)

    def __str__(self):
        return self.url

