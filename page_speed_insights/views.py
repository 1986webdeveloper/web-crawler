"""
    Import needed things
"""
import json
import os
import urllib.request
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse

from domain.models import DomainUrl, Domain
from .models import PageSeedInsight
from .task import send_report_status
from ajax_datatable.views import AjaxDatatableView


def report_data(request, pk):
    """
       report_data for done report
    """
    domain = Domain.objects.get(id=pk)
    exists = PageSeedInsight.objects.filter(domain_fk=pk).exists()
    return render(request, "pagespeed/report.html", {"exists": exists, "domain": domain})


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


def flag_data(request, pk):
    """
           Flag Data for cron
    """
    data = request.POST["flag"]
    PageSeedInsight.objects.filter(domain_fk=pk).update(cron_flag = data)
    return JsonResponse({"message": "Status updated successfully!!"})


class PageInsightAjaxDatatableView(AjaxDatatableView):

    model = PageSeedInsight
    title = 'Page Insight Data'
    initial_order = [["url", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'url', 'visible': True, },
        {'name': 'action', 'visible': True, 'searchable': False, "orderable": False},
    ]

    def get_initial_queryset(self, request=None):
        domain_id = self.request.resolver_match.kwargs.get('pk')
        return self.model.objects.filter(domain_fk_id=domain_id)

    def customize_row(self, row, obj):
        text = f"""<a href="{reverse('page_speed_insights:detail_data', args=(obj.id,))}" target="_blank">View</a>"""
        row['action'] = text
