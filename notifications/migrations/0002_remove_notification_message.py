# Generated by Django 3.2.5 on 2021-08-12 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='message',
        ),
    ]
