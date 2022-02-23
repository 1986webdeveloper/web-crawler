from django.contrib import admin
from .models import PageSeedInsight


class PageSeedInsightAdmin(admin.ModelAdmin):
    list_display = ("id", "url", "domain", "result", "cron_flag")


admin.site.register(PageSeedInsight, PageSeedInsightAdmin)
