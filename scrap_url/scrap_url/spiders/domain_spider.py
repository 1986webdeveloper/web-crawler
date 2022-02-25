"""
    Import needed things
"""
from urllib.parse import urlparse
import logging
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
import xmltodict
from domain import tasks
from scrap_url.scrap_url.items import ScrapUrlItem
from domain.models import Domain


class DomainLinkSpider(scrapy.Spider):
    """
        crawl domain url
    """
    name = "Domain-Link-spider"
    start_urls = []

    def __init__(self, *args, **kwargs):
        """
            __init__ method for DomainLinkSpider
        """
        super(DomainLinkSpider, self).__init__(*args, **kwargs)
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.domain_id = kwargs.get('domain_id')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        self.links = set()
        self.domain_name = self.domain
        self.domain_obj = Domain.objects.get(id=self.domain_id)

    def start_requests(self):
        """
               start_requests
        """
        yield Request(self.url)
        yield Request(self.sitemap_url(), callback=self.parse_xml)

    def parse_xml(self, response):
        """
            parse_xml for sitemap
        """
        site_map = xmltodict.parse(response.text)
        urls = [url["loc"] for url in site_map["urlset"]["url"]]
        for url in urls:
            if url == self.sitemap_url():
                continue
            self.store_in_db(url=url)
            self.links.add(url)
            yield response.follow(url, self.parse)

    def parse(self, response, **kwargs):
        """
             parse
        """
        link_extractor = LinkExtractor()
        for link in link_extractor.extract_links(response):
            if link.url == self.sitemap_url():
                continue
            parsed_url = urlparse(link.url)
            if parsed_url.netloc == self.domain_name:
                if link.url not in self.links:
                    self.store_in_db(url=link.url)
                    self.links.add(link.url)
                    yield response.follow(link, self.parse)

    def store_in_db(self, url):
        """
             Data store
        """
        scrap_url_item = ScrapUrlItem()
        scrap_url_item["url"] = url
        scrap_url_item["domain"] = self.domain_obj
        try:
            scrap_url_item.save()
        except:
            pass

    def sitemap_url(self):
        return self.url + "/sitemap.xml"

    def close(self, spider, reason):
        """
                Close scrapper
        """

        tasks.scrapp_insight_data_in_domain.delay(spider.domain_id,)
