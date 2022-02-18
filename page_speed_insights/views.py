from django.shortcuts import redirect
from domain.models import DomainUrl
import os
import urllib.request
import json
from django.shortcuts import render
from .models import PageSeedInsight

# Create your views here.


def report_data(request):
    queryset = PageSeedInsight.objects.filter(domain='http://acquaintsoft.com')
    context={}
    context['data'] = queryset
    return render(request, "pagespeed/report.html", context)


def page_speed_scrap_url(request, domain_obj):
    urls = DomainUrl.objects.filter(domain__name=domain_obj.name)
    for i in urls:
        google_speed_page_url = os.environ['PAGESPEED_URLS'] + '?url=' + i.url + '&key=' + os.environ['PAGESPEED_KEY']
        page_speed_insights_response = urllib.request.urlopen(google_speed_page_url)
        convert_to_json = json.loads(page_speed_insights_response.read())
        PageSeedInsight.objects.create(url=i.url, domain=i.domain.name, result=convert_to_json)
    return redirect("page_speed_insights:report")


def detail_report_data(request, pk):
    queryset = PageSeedInsight.objects.filter(id=pk)
    context = {}
    context['data'] = queryset
    return render(request, "pagespeed/report_data.html", context)