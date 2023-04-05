# Generated by Django 4.1.6 on 2023-02-07 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_bid_userbid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='maxbid',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='winbid', to='auctions.bid'),
        ),
    ]