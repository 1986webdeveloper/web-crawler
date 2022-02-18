from urllib.parse import urlparse
from scrap_url.scrap_url.spiders.domain import DomainLinkSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def get_domain_name_from_url(domain_url):
    parsed_url = urlparse(domain_url)
    return parsed_url.netloc


def scrap_url(domain_obj):
    domain_name = get_domain_name_from_url(domain_obj.name)
    process = CrawlerProcess(get_project_settings())
    process.crawl(DomainLinkSpider, url=domain_obj.name, domain=domain_name,
                  domain_id=domain_obj.id)
    process.start(stop_after_crawl=False)
