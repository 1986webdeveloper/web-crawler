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
    """Domain table"""
    STATUS_CHOICES = (
        (0, "Fetching Url"),
        (1, "Fetching Page Speed Data"),
        (2, "Done"),
    )
    name = models.URLField()
    user = models.ForeignKey(User, related_name="domains",
                             on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return str(self.name)


class DomainUrl(TimeStampModel):
    """
        DomainUrl is for storing data of domain name and url
    """
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    url = models.CharField(max_length=1024)

    class Meta:
        """
              Meta for unique_together
        """
        unique_together = ("domain", "url")
