# Generated by Django 3.2.6 on 2022-02-21 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0017_rename_tagassigned_detailstags'),
    ]

    operations = [
        migrations.DeleteModel(
            name='addressTags',
        ),
    ]
