from urllib.parse import urlparse

from domain.scrap import DomainUrlScrapper
from scrap_url.scrap_url.spiders.domain import LinkSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from domain.models import Domain, DomainUrl


def get_domain_name_from_url(domain_url):
    parsed_url = urlparse(domain_url)
    return parsed_url.netloc


def scrap_url(url):
    domain_name = get_domain_name_from_url(url)
    process = CrawlerProcess(get_project_settings())
    process.crawl(LinkSpider, url=url, domain=domain_name)
    process.start()


def scrap_and_store_url(domain):
    scrapper = DomainUrlScrapper(domain.name)
    url_list = scrapper.scrap()
    for url in url_list:
        DomainUrl.objects.get_or_create(domain=domain,
                                        url=url)
