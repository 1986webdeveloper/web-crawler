from domain.models import Domain
from celery import shared_task
from domain.scrapping_service import scrap_url


@shared_task(name="scrapp_url_in_domain")
def scrapp_url_in_domain(domain_obj_id):
    try:
        obj = Domain.objects.get(id=domain_obj_id)
        scrap_url(obj)
    except Domain.DoesNotExist:
        pass
