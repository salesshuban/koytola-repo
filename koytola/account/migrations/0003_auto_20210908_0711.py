# Generated by Django 3.1 on 2021-09-08 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210818_0631'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_buyer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='linkedin_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
