"""domain spider service"""

from urllib.parse import urlparse
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
import xmltodict
from domain import tasks
from scrap_url.scrap_url.items import ScrapUrlItem
from domain.models import Domain


class DomainLinkSpider(scrapy.Spider):
    """domain link spider is a spider for collecting url"""
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
        """start scrapping"""
        yield Request(self.sitemap_url(), callback=self.parse_xml)
        yield Request(self.url)

    def parse_xml(self, response):
        """parse xml response and get url in response"""
        try:
            site_map = xmltodict.parse(response.text)
            urls = [url["loc"] for url in site_map["urlset"]["url"]]
        except Exception as e:
            urls = []
        for url in urls:
            if url == self.sitemap_url():
                continue
            if url not in self.links:
                self.store_in_db(url=url)
                self.links.add(url)
                yield response.follow(url, self.parse)

    def parse(self, response, **kwargs):
        """parse response find all url in page with same domain.
         crawl not visited url"""
        link_extractor = LinkExtractor()
        for link in link_extractor.extract_links(response):
            if link.url == self.sitemap_url():
                continue
            parsed_url = urlparse(link.url)
            if parsed_url.netloc == self.domain_name and link.url not in self.links:
                self.store_in_db(url=link.url)
                self.links.add(link.url)
                yield response.follow(link, self.parse)

    def store_in_db(self, url):
        """store url in database"""
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
        """Close scrapper"""
        tasks.scrapp_insight_data_in_domain.delay(spider.domain_id, )
