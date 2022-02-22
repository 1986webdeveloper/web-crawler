from django.contrib import admin
from domain.models import Domain, Url, DomainUrl


class DomainModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name")


class UrlModelAdmin(admin.ModelAdmin):
    list_display = ("url", "domain")


class DomainUrlModelAdmin(admin.ModelAdmin):
    list_display = ("url", "domain")
    search_fields = ("url", )


admin.site.register(Domain, DomainModelAdmin)
admin.site.register(Url, UrlModelAdmin)
admin.site.register(DomainUrl, DomainUrlModelAdmin)
