from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import WallapopSearch
import logging

log = logging.getLogger("app_logger")


@receiver(post_save, sender=WallapopSearch)
def handle_search_scheduling(sender, instance, created, **kwargs):
    log.debug(f"Received signal from {sender} with instance {instance}")
    instance.schedule_task()
