# Generated by Django 3.2.6 on 2022-02-21 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0014_addresstags'),
    ]

    operations = [
        migrations.CreateModel(
            name='addressDetailsTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagName', models.CharField(max_length=100)),
            ],
        ),
    ]
