from urllib.parse import urlparse

from scrap_url.scrap_url.spiders.domain import LinkSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def get_domain_name_from_url(domain_url):
    parsed_url = urlparse(domain_url)
    return parsed_url.netloc


def scrap_url(url):
    domain_name = get_domain_name_from_url(url)
    process = CrawlerProcess(get_project_settings())
    process.crawl(LinkSpider, url=url, domain=domain_name)
    process.start()
