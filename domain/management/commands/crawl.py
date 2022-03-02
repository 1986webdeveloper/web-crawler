"""
    Import needed things
"""
from django.core.management.base import BaseCommand

from domain.models import Domain
from domain.tasks import scrapp_url_in_domain


class Command(BaseCommand):
    """
        Management command for domain url
    """
    help = "Release the spiders"

    def handle(self, *args, **options):
        for domain in Domain.objects.filter(is_fetched=False):
            scrapp_url_in_domain(domain.id)
            domain.is_fetched = True
            domain.save()