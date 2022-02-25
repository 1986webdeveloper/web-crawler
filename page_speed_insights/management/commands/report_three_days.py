"""
import needed things
"""
import datetime
import urllib.request
import json
import os
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from domain.models import DomainUrl
from page_speed_insights.models import PageSeedInsight
from page_speed_insights.task import send_report_status

# Create your views here.


class Command(BaseCommand):
    """
      Command for storing url using cron
    """
    @transaction.atomic
    def handle(self, *args, **options):
        urls = DomainUrl.objects.all()
        email = User.objects.filter(email=urls[0].domain.user.email)
        for i in urls:
            try:
                report_exists = PageSeedInsight.objects.filter(url=i)
                current = datetime.datetime.now()
                running = report_exists[0].created_at + datetime.timedelta(days=3)
                if current == running and report_exists.cron_flag is True:
                    google_speed_page_url = os.environ['PAGESPEED_URLS'] + '?url=' + i.url \
                                            + '&key=' + \
                                            os.environ['PAGESPEED_KEY']
                    page_speed_insights_response = urllib.request.urlopen(google_speed_page_url)
                    convert_to_json = json.loads\
                        (page_speed_insights_response.read())
                    PageSeedInsight.objects.create(url=i.url,
                                                   domain=i.domain.name,
                                                   result=convert_to_json)
            except Exception as error:
                logging.exception(error)
                continue
        email = email[0]
        send_report_status(email)