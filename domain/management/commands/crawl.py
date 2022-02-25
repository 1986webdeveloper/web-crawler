"""
    Import needed things
"""
from django.core.management.base import BaseCommand

from domain.models import Domain
from domain.scrapping_service import scrap_url


class Command(BaseCommand):
    """
        Management command for domain url
    """
    help = "Release the spiders"

    def handle(self, *args, **options):
        for domain in Domain.objects.filter(is_fetched=False):
            scrap_url(domain.name)
            domain.is_fetched = True
            domain.save()