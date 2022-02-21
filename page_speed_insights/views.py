from domain.models import DomainUrl
import os
import urllib.request
import json
from django.shortcuts import render
from scrapper.settings import BASE_DIR
from .models import PageSeedInsight
from rest_framework.exceptions import NotFound

# Create your views here.


def report_data(request):
    queryset = PageSeedInsight.objects.filter(domain='http://acquaintsoft.com')
    context={}
    context['data'] = queryset
    return render(request, "pagespeed/report.html", context)


def detail_report_data(request, pk):
    queryset = PageSeedInsight.objects.filter(id=pk)
    context = {}
    context['data'] = queryset
    return render(request, "pagespeed/report_data.html", context)


def page_speed_scrap_url(obj):
    f = open(os.path.join(BASE_DIR, "test2.log"), "a+")
    f.write("test12")
    f.close()
    urls = DomainUrl.objects.filter(domain=obj)
    f = open(os.path.join(BASE_DIR, "test3.log"), "a+")
    len_ = len(urls)
    f.write(f"{len_}")
    f.close()
    for i in urls:
        try:
            google_speed_page_url = os.environ['PAGESPEED_URLS'] + '?url=' + i.url + '&key=' + os.environ['PAGESPEED_KEY']
            page_speed_insights_response = urllib.request.urlopen(google_speed_page_url)
            convert_to_json = json.loads(page_speed_insights_response.read())
            PageSeedInsight.objects.create(url=i.url, domain=i.domain.name, result=convert_to_json)
        except Exception as e:
            f = open(os.path.join(BASE_DIR, "exception.log"), "a+")
            f.writelines(str(e))
            f.close()
            raise NotFound("Something went wrong")

