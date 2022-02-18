from django.contrib import admin
from .models import PageSeedInsight


class PageSeedInsightAdmin(admin.ModelAdmin):
    list_display = ("url", "domain", "result")


admin.site.register(PageSeedInsight, PageSeedInsightAdmin)
