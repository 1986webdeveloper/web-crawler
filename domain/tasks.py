"""
    Import Domain model from Domain
"""
from celery import shared_task
from domain.models import Domain
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrap_url.scrap_url.spiders.domain_spider import DomainLinkSpider
from scrap_url.scrap_url.spiders.page_speed_spider import PageSpeedSpider


def get_domain_name_from_url(domain_url):
    """
       get_domain_name_from_url for getting domain url
    """
    parsed_url = urlparse(domain_url)
    return parsed_url.netloc


@shared_task(name="scrapp_url_in_domain")
def scrapp_url_in_domain(domain_obj_id):
    """
        scrapp_url_in_domain is use for scraping url from domain
    """
    try:
        obj = Domain.objects.get(id=domain_obj_id)
        domain_name = get_domain_name_from_url(obj.name)
        process = CrawlerProcess(get_project_settings())
        process.crawl(DomainLinkSpider, url=obj.name, domain=domain_name,
                      domain_id=obj.id)
        process.start(stop_after_crawl=False)
    except Domain.DoesNotExist:
        pass


@shared_task(name="scrapp_insight_data_in_domain")
def scrapp_insight_data_in_domain(domain_obj_id):
    """
           scrapp_insight_data_in_domain is use for scraping url from domain
    """
    try:
        obj = Domain.objects.get(id=domain_obj_id)
        obj.status = 1
        obj.save()
        process = CrawlerProcess(get_project_settings())
        process.crawl(PageSpeedSpider, domain_id=obj.id)
        process.start(stop_after_crawl=False)
    except Domain.DoesNotExist:
        pass
