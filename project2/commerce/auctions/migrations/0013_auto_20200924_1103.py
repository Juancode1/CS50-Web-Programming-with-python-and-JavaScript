# Generated by Django 3.0.3 on 2020-09-24 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_listing_terminated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sold',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
