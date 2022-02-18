from django.shortcuts import redirect
from domain.models import Url
import os
import urllib.request
import json
from django.shortcuts import render
from .models import PageSeedInsight

# Create your views here.


def report_data(request):
    queryset = PageSeedInsight.objects.filter(domain='acquaintsoft.com')
    context={}
    context['data'] = queryset
    return render(request, "pagespeed/report.html", context)


def page_speed_scrap_url(request, domain_name):
    urls = Url.objects.filter(domain=domain_name)
    for i in urls:
        google_speed_page_url = os.environ['PAGESPEED_URLS'] + '?url=' + i.url + '&key=' + os.environ['PAGESPEED_KEY']
        page_speed_insights_response = urllib.request.urlopen(google_speed_page_url)
        convert_to_json = json.loads(page_speed_insights_response.read())
        PageSeedInsight.objects.create(url=i.url, domain=i.domain, result=convert_to_json)
    return redirect("page_speed_insights:report")

