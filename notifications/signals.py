from django.db.models.signals import post_save, post_delete, m2m_changed
from django.db.models import Q
from django.dispatch import receiver
from .models import Notification, NotificationType
from jobs.models import Job
from stocks.models import StockTransfer, StockReceipts, StockItem
from profiles.models import UserTypes, UserProfile 


def create_notification(user, notification_type, job=None, stock_item=None):
    """
    Function to create notification.
    """
    if notification_type == 'Job Alert':
        if job:
            count = Notification.objects.filter(user=user, job=job).count()
            if count == 0:
                Notification.objects.create(
                    user=user,
                    type=NotificationType.objects.get(type='New Job Alert'),
                    job=Job.objects.get(id=job.id)
                )
    elif notification_type == 'Stock Alert':
        if stock_item:
            Notification.objects.create(
                user=user,
                type=NotificationType.objects.get(type='Stock Warning'),
                stock_item=StockItem.objects.get(id=stock_item.id)
            )


@receiver(m2m_changed, sender=Job.assigned_to.through)
def job_alert(sender, instance, pk_set, action, **kwargs):
    """
    Function to create notification for job.
    """
    if action == 'post_add':
        for job_user in instance.assigned_to.all():
            create_notification(job_user, 'Job Alert', job=instance)


