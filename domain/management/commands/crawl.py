from django.core.management.base import BaseCommand
from domain.scrapping_service import scrap_url


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        url = "http://acquaintsoft.com/"
        scrap_url(url)