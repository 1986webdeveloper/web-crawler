# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
"""
    Import needed things
"""
from scrapy_djangoitem import DjangoItem
from domain.models import DomainUrl


class ScrapUrlItem(DjangoItem):
    """
        Import needed things
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = DomainUrl
