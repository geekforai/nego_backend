
from requistion.models import Requisition
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_welcome_email

@receiver(post_save, sender=Requisition)
def schedule_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_welcome_email(instance.id)  # Schedule the task
