from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import WallapopSearch


@receiver(post_save, sender=WallapopSearch)
def handle_search_scheduling(sender, instance, created, **kwargs):
    instance.schedule_task()
