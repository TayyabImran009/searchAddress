# Generated by Django 3.2.6 on 2022-02-17 18:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('User', '0009_auto_20220217_0340'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressdetails',
            name='numberChecked',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
