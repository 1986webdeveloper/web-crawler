"""
    below urlparse for getting name
"""
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrap_url.scrap_url.spiders.domain_spider import DomainLinkSpider


def get_domain_name_from_url(domain_url):
    """
       get_domain_name_from_url for getting domain url
    """
    parsed_url = urlparse(domain_url)
    return parsed_url.netloc


def scrap_url(domain_obj):
    """
           scrap_url and storing domain url
    """
    domain_name = get_domain_name_from_url(domain_obj.name)
    process = CrawlerProcess(get_project_settings())
    process.crawl(DomainLinkSpider, url=domain_obj.name, domain=domain_name,
                  domain_id=domain_obj.id)
    process.start(stop_after_crawl=False)
