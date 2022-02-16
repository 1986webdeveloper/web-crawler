# import scrapy
#
#
# class DomainSpider(scrapy.Spider):
#     name = 'domain'
#     allowed_domains = ['domain.com']
#     start_urls = ['http://domain.com/']
#
#     # def __init__(self, *args, **kwargs):
#     #     self.url = kwargs.get('url')
#     #     self.domain = kwargs.get('domain')
#     #     self.start_urls = [self.url]
#     #     self.allowed_domains = [self.domain]
#
#     def parse(self, response):
#         pass

import scrapy
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

from scrap_url.scrap_url.items import ScrapUrlItem


class TheodoSpider(scrapy.Spider):
    name = "theodo"
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(TheodoSpider, self).__init__(*args, **kwargs)
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        self.links = set(self.start_urls)
        self.domain_name = self.domain

    def parse(self, response):
        le = LinkExtractor()
        for link in le.extract_links(response):
            parsed_url = urlparse(link.url)
            if parsed_url.netloc == self.domain_name:
                if link.url not in self.links:
                    self.store_in_db(url=link.url, domain=self.domain_name)
                    self.links.add(link.url)
                    yield response.follow(link, self.parse)

    def store_in_db(self, url, domain):
        s = ScrapUrlItem()
        s["url"] = url
        s["domain"] = domain
        s.save()
