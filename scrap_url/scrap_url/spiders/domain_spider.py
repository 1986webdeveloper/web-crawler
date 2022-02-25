import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

from domain.models import Domain
from domain import tasks
from scrap_url.scrap_url.items import ScrapUrlItem
import xmltodict


class DomainLinkSpider(scrapy.Spider):
    name = "Domain-Link-spider"
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(DomainLinkSpider, self).__init__(*args, **kwargs)
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.domain_id = kwargs.get('domain_id')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        self.links = set(self.start_urls)
        self.domain_name = self.domain
        self.domain_obj = Domain.objects.get(id=self.domain_id)

    def start_requests(self):
        xml_url = self.url + "/sitemap.xml"
        yield Request(xml_url, callback=self.parse_xml)
        yield Request(self.url)

    def parse_xml(self, response):
        site_map = xmltodict.parse(response.text)
        urls = [url["loc"] for url in site_map["urlset"]["url"]]
        for url in urls:
            self.store_in_db(url=url)
            self.links.add(url)
            yield response.follow(url, self.parse)

    def parse(self, response):
        le = LinkExtractor()
        for link in le.extract_links(response):
            parsed_url = urlparse(link.url)
            if parsed_url.netloc == self.domain_name:
                if link.url not in self.links:
                    self.store_in_db(url=link.url)
                    self.links.add(link.url)
                    yield response.follow(link, self.parse)

    def store_in_db(self, url):
        s = ScrapUrlItem()
        s["url"] = url
        s["domain"] = self.domain_obj
        try:
            s.save()
        except:
            pass

    def close(spider, reason):
        tasks.scrapp_insight_data_in_domain.delay(spider.domain_id,)
