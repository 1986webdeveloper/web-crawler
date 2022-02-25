from domain.models import Domain
from celery import shared_task
from domain.scrapping_service import scrap_url
from page_speed_insights.views import page_speed_scrap_url


@shared_task(name="scrapp_url_in_domain")
def scrapp_url_in_domain(domain_obj_id):
    try:
        obj = Domain.objects.get(id=domain_obj_id)
        scrap_url(obj)
    except Domain.DoesNotExist:
        pass


@shared_task(name="scrapp_insight_data_in_domain")
def scrapp_insight_data_in_domain(domain_obj_id):
    try:
        obj = Domain.objects.get(id=domain_obj_id)
        page_speed_scrap_url(obj)
    except Domain.DoesNotExist:
        pass
