# Generated by Django 3.0.2 on 2020-03-15 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worktracker', '0020_break'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstat',
            name='current_side_track',
            field=models.TextField(default='side_track_list', null=True),
        ),
    ]