# Generated by Django 3.0.2 on 2020-02-23 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worktracker', '0014_auto_20200223_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='temp_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
