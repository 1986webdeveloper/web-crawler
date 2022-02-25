"""
      Import Models From Django db
"""
from django.db import models
from django.contrib.auth.models import User


class TimeStampModel(models.Model):
    """
          TimeStampModel For datetime
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
             Meta For abstract
        """
        abstract = True


class Domain(TimeStampModel):
    """
            Domain Details
    """
    DoesNotExist = None
    objects = None
    name = models.URLField()
    user = models.ForeignKey(User, related_name="domains",
                             on_delete=models.CASCADE)
    is_fetched = models.BooleanField(default=False)

    class Meta:
        """
             Meta For unique_together
        """
        unique_together = ("name", "user",)

    def __str__(self):
        return str(self.name)

    @property
    def status(self):
        """
            Status Of fetching url
        """
        return "FETCHING URL"


class DomainUrl(TimeStampModel):
    """
        DomainUrl is for storing data of domain name and url
    """
    objects = None
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    url = models.CharField(max_length=1024)

    class Meta:
        """
              Meta for unique_together
        """
        unique_together = ("domain", "url")


class Url(TimeStampModel):
    """
         Storing Url Data
    """
    url = models.CharField(max_length=1024)
    domain = models.CharField(max_length=255)

    def __str__(self):
        return str(self.url)
