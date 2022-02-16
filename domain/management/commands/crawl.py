from django.core.management.base import BaseCommand
from scrap_url.scrap_url.spiders.domain import TheodoSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        url = "http://acquaintsoft.com/"
        domain = "acquaintsoft.com"
        process = CrawlerProcess(get_project_settings())
        process.crawl(TheodoSpider, url=url, domain=domain)
        process.start()
