# Generated by Django 3.0.2 on 2020-02-22 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worktracker', '0006_auto_20200222_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='ending',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='notes',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='tags',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='timetaken',
            field=models.DurationField(blank=True, null=True),
        ),
    ]