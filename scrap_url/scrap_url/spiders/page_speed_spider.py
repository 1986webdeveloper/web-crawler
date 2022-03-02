"""page speed spider service"""

import os
import scrapy
from scrapy import Request

from page_speed_insights.task import send_report_status
from scrap_url.scrap_url.items import PageSeedInsightItem
from domain.models import Domain, DomainUrl


class PageSpeedSpider(scrapy.Spider):
    """PageSpeedSpider"""
    name = "PageSpeedSpider"
    start_urls = []

    def __init__(self, *args, **kwargs):
        """ initialize object"""
        super(PageSpeedSpider, self).__init__(*args, **kwargs)
        self.domain_id = kwargs.get('domain_id')
        self.domain_obj = Domain.objects.get(id=self.domain_id)

    def start_requests(self):
        """start scrapping"""
        base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?key=" + os.environ['PAGESPEED_KEY']
        for obj in DomainUrl.objects.filter(domain=self.domain_obj):
            google_speed_page_url = base_url + '&url=' + obj.url
            yield Request(google_speed_page_url)

    def parse(self, response, **kwargs):
        """parse response find all url in page with same domain.
         crawl not visited url"""
        try:
            url = response.url.split("&url=")[1]
            self.store_in_db(url, response.json())
        except:
            pass

    def store_in_db(self, url, json):
        """store url in database"""
        scrap_url_item = PageSeedInsightItem()
        scrap_url_item["url"] = url
        scrap_url_item["domain_fk"] = self.domain_obj
        scrap_url_item["domain"] = self.domain_obj.name
        scrap_url_item["result"] = json
        try:
            scrap_url_item.save()
        except:
            pass

    def close(self, spider, reason):
        """Close scrapper"""
        domain = spider.domain_obj
        domain.status = 2
        domain.save()
        send_report_status(domain.user)
