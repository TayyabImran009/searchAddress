# Generated by Django 3.2.6 on 2022-02-16 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_useraddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddress',
            name='fName',
        ),
        migrations.RemoveField(
            model_name='useraddress',
            name='lName',
        ),
    ]
