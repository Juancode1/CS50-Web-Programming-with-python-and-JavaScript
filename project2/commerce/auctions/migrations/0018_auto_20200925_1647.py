# Generated by Django 3.0.3 on 2020-09-25 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20200925_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='terminated',
            field=models.BooleanField(default=False),
        ),
    ]
