# Generated by Django 3.2.5 on 2021-08-07 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20210807_1038'),
        ('jobs', '0008_auto_20210801_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.project'),
        ),
    ]
