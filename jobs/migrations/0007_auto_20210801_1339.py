# Generated by Django 3.2.5 on 2021-08-01 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20210801_1339'),
        ('jobs', '0006_alter_job_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='assigned_to',
            field=models.ManyToManyField(blank=True, related_name='assigned_to', to='profiles.UserProfile'),
        ),
        migrations.AlterField(
            model_name='job',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.userprofile'),
        ),
        migrations.AlterField(
            model_name='jobtimes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.userprofile'),
        ),
    ]