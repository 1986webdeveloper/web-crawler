"""
    Import needed things
"""
from urllib.parse import urlparse
import logging
import scrapy
from scrapy.linkextractors import LinkExtractor
import xmltodict
import requests
from domain.models import Domain, DomainUrl
from domain import tasks
from scrap_url.scrap_url.items import ScrapUrlItem


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
        self.links = set(self.start_urls)
        self.domain_name = self.domain
        self.domain_obj = Domain.objects.get(id=self.domain_id)

    def parse(self, response, **kwargs):
        """
             Crawl all url from domain
        """
        link_extractor = LinkExtractor()
        for link in link_extractor.extract_links(response):
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
        name = self.domain_obj.name
        sitemap_url = name + "/sitemap.xml"
        try:
            scrap_url_item.save()
            if sitemap_url:
                # below line is for convert sitemap.xmlto dict
                site_map = xmltodict.parse(requests.get(scrap_url_item["url"]).text)
                # below line is get all url from dict
                urls = [url["loc"] for url in site_map["urlset"]["url"]]
                # below for loop is store all missing url in database which
                # is get from sitemap.xml missing from crawl
                for i in urls:
                    DomainUrl.objects.get_or_create(domain=self.domain_obj, url=i)
        except Exception as error:
            logging.exception(error)

    def close(self, spider, reason):
        """
                Close scrapper
        """

        tasks.scrapp_insight_data_in_domain.delay(spider.domain_id,)
