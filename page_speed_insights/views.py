"""
    Import needed things
"""
import json
import os
import urllib.request
import logging
from django.shortcuts import render
from django.contrib.auth.models import User
from domain.models import DomainUrl
from .models import PageSeedInsight
from .task import send_report_status


def report_data(request, pk):
    """
       report_data for done report
    """
    queryset = PageSeedInsight.objects.filter(domain_fk=pk)
    return render(request, "pagespeed/report.html", {"data" : queryset})


def detail_report_data(request, pk):
    """
         detail_report_data for done report
    """
    queryset = PageSeedInsight.objects.filter(id=pk)
    context = {}
    context['data'] = queryset
    return render(request, "pagespeed/report_data.html", context)


def page_speed_scrap_url(obj):
    """
            page_speed_scrap_url for google speed page API
    """
    email = User.objects.filter(email=obj.user.email).first()
    urls = DomainUrl.objects.filter(domain=obj)

    for i in urls:
        try:
            google_speed_page_url = os.environ['PAGESPEED_URLS'] + '?url=' + i.url + '&key=' \
                                    + os.environ['PAGESPEED_KEY']
            page_speed_insights_response = urllib.request.urlopen(google_speed_page_url)
            convert_to_json = json.loads(page_speed_insights_response.read())
            PageSeedInsight.objects.create(url=i.url, domain=i.domain.name, result=convert_to_json, domain_fk=obj)
        except Exception as error:
            logging.exception(error)
            continue

    obj.status = 2
    obj.save()
    send_report_status(email)


def flag_data(request):
    """
           Flag Data for cron
    """
    data = request.POST["flag"]
    queryset = PageSeedInsight.objects.all()
    for i in queryset:
        i.cron_flag = data
        i.save()
    return render(request, "pagespeed/report.html")
