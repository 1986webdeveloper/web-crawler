# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
"""Scrapper items"""
from scrapy_djangoitem import DjangoItem
from domain.models import DomainUrl


class ScrapUrlItem(DjangoItem):
    """ Scrap url item connect with django model Domain url"""
    django_model = DomainUrl