# Generated by Django 3.0.2 on 2020-06-28 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_log', '0003_auto_20200628_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='app_history',
            name='tittle',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
