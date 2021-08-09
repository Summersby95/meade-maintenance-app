import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PPM
from jobs.models import Job, JobStatus, JobTypes, JobPriority


def create_job_from_ppm(ppm, due_date):
    """ Function to create a new job from a PPM. """
    Job.objects.create(
        job_title=ppm.job_title,
        department=ppm.asset.department,
        type=JobTypes.objects.get(type='General Maintenance'),
        status=JobStatus.objects.get(status='Not Started'),
        due_date=due_date,
        asset=ppm.asset,
        ppm=ppm,
        created_by=ppm.created_by,
        priority=JobPriority.objects.get(priority='Medium'),
        description=ppm.description,
    )


@receiver(post_save, sender=PPM)
def create_job_from_ppm_signal(sender, instance, created, **kwargs):
    """ Signal to create a job from a PPM. """
    print(instance)
    if created:
        create_job_from_ppm(instance, datetime.date.today())


@receiver(post_save, sender=Job)
def duplicate_job_if_ppm(sender, instance, created, **kwargs):
    if created==False and instance.ppm and instance.status.status == "Completed":
        create_job_from_ppm(instance.ppm, datetime.date.today()+datetime.timedelta(days=instance.ppm.time_interval))
