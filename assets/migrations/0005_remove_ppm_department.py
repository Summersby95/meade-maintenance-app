# Generated by Django 3.2.5 on 2021-08-08 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_remove_ppm_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ppm',
            name='department',
        ),
    ]