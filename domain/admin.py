"""
    Import admin model for showing details of admin
"""
from django.contrib import admin
from domain.models import Domain, Url, DomainUrl


class DomainModelAdmin(admin.ModelAdmin):
    """
        Getting DomainModelAdmin Details
    """
    list_display = ("id", "user", "name")


class UrlModelAdmin(admin.ModelAdmin):
    """
           Getting UrlModelAdmin Details
    """
    list_display = ("url", "domain")


class DomainUrlModelAdmin(admin.ModelAdmin):
    """
            Getting DomainUrlModelAdmin Details
    """
    list_display = ("url", "domain")
    search_fields = ("url", )


admin.site.register(Domain, DomainModelAdmin)
admin.site.register(Url, UrlModelAdmin)
admin.site.register(DomainUrl, DomainUrlModelAdmin)
