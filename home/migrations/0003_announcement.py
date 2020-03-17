# Generated by Django 3.0.3 on 2020-02-07 08:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0002_appdetails_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announcement', models.CharField(max_length=50)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('date_completed_by', models.DateField()),
                ('completed', models.CharField(choices=[('True', 'Work completed'), ('False', 'Work not done')], max_length=5)),
                ('url', models.CharField(max_length=50)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]