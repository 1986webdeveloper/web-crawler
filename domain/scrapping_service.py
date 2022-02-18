from urllib.parse import urlparse

from scrap_url.scrap_url.spiders.domain import LinkSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from page_speed_insights.views import page_speed_scrap_url, report_data

def get_domain_name_from_url(domain_url):
    parsed_url = urlparse(domain_url)
    return parsed_url.netloc


def scrap_url(url):
    domain_name = get_domain_name_from_url(url)
    process = CrawlerProcess(get_project_settings())
    process.crawl(LinkSpider, url=url, domain=domain_name)
    process.start()
    page_speed_scrap_url(url, domain_name)
    # report_data(url, domain_name)
