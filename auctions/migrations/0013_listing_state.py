# Generated by Django 4.1.6 on 2023-02-04 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_remove_watchlist_userlist_listing_createdlist_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='state',
            field=models.BooleanField(default=True),
        ),
    ]