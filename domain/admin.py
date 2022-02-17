from django.contrib import admin
from domain.models import Domain, Url, DomainUrl


class DomainModelAdmin(admin.ModelAdmin):
    list_display = ("user", "name")

class UrlModelAdmin(admin.ModelAdmin):
    list_display = ("url", "domain")

class DomainUrlModelAdmin(admin.ModelAdmin):
    list_display = ("url", "domain")


admin.site.register(Domain, DomainModelAdmin)
admin.site.register(Url, UrlModelAdmin)
admin.site.register(DomainUrl, DomainUrlModelAdmin)
