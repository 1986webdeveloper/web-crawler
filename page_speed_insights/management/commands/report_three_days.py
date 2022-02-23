from domain.models import DomainUrl
import os
import urllib.request
import json
from scrapper.settings import BASE_DIR
from page_speed_insights.models import PageSeedInsight
from page_speed_insights.task import send_report_status
from django.contrib.auth.models import User
import datetime
from django.core.management.base import BaseCommand
from django.db import transaction

# Create your views here.


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        f = open(os.path.join(BASE_DIR, "test2.log"), "a+")
        f.write("test12")
        f.close()
        urls = DomainUrl.objects.all()
        f = open(os.path.join(BASE_DIR, "test3.log"), "a+")
        len_ = len(urls)
        f.write(f"{len_}")
        f.close()
        email = User.objects.filter(email=urls[0].domain.user.email)
        for i in urls:
            try:
                report_exists = PageSeedInsight.objects.filter(url=i)
                current = datetime.datetime.now()
                running = report_exists[0].created_at + datetime.timedelta(days=3)
                if current == running and report_exists.cron_flag == True:
                    google_speed_page_url = os.environ['PAGESPEED_URLS'] + '?url=' + i.url + '&key=' + os.environ['PAGESPEED_KEY']
                    page_speed_insights_response = urllib.request.urlopen(google_speed_page_url)
                    convert_to_json = json.loads(page_speed_insights_response.read())
                    PageSeedInsight.objects.create(url=i.url, domain=i.domain.name, result=convert_to_json)
            except Exception as e:
                f = open(os.path.join(BASE_DIR, "exception.log"), "a+")
                f.writelines(str(e))
                f.close()
                continue
        Email = email[0]
        send_report_status(Email)
