"""
    Import admin model for showing details of admin
"""
from django.contrib import admin
from domain.models import Domain, DomainUrl


class DomainModelAdmin(admin.ModelAdmin):
    """
        Getting DomainModelAdmin Details
    """
    list_display = ("id", "user", "name", "status")


class UrlModelAdmin(admin.ModelAdmin):
    """
           Getting UrlModelAdmin Details
    """
    list_display = ("id", "url", "domain")


class DomainUrlModelAdmin(admin.ModelAdmin):
    """
            Getting DomainUrlModelAdmin Details
    """
    list_display = ("id", "url", "domain")
    search_fields = ("url", "domain__name")


admin.site.register(Domain, DomainModelAdmin)
admin.site.register(DomainUrl, DomainUrlModelAdmin)
