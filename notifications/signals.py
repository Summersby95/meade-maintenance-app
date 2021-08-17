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
            count = Notification.objects.filter(
                user=user,
                job=job,
                type=NotificationType.objects.get(type='New Job Alert')
            ).count()
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


@receiver(post_save, sender=StockTransfer)
def stock_alert(sender, instance, created, **kwargs):
    """
    Function to create notification for stock.
    """
    if instance.item.get_current_stock() < instance.item.stock_alert:
        notify_users = UserProfile.objects.filter(
            Q(user_type=UserTypes.objects.get(type='Stock Controller')) |
            Q(user_type=UserTypes.objects.get(type='Manager')) |
            Q(user_type=UserTypes.objects.get(type='Admin'))
        )
        for stock_user in notify_users:
            create_notification(stock_user.user, 'Stock Alert',
                                stock_item=instance.item)


@receiver(post_save, sender=StockTransfer)
def unassigned_stock_alert(sender, instance, created, **kwargs):
    """
    Function to create notification for unassigned stock
    """
    if created:
        if instance.job is None:
            create_notification(instance.user, 'Unassigned Stock Alert')


