# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
"""Scrapper items"""
from scrapy_djangoitem import DjangoItem
from domain.models import DomainUrl
from page_speed_insights.models import PageSeedInsight


class ScrapUrlItem(DjangoItem):
    """ Scrap url item connect with django model Domain url"""
    django_model = DomainUrl


class PageSeedInsightItem(DjangoItem):
    django_model = PageSeedInsight
