# Generated by Django 4.2.3 on 2023-12-24 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='config',
            field=models.JSONField(blank=True, default={}),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='schema',
            field=models.JSONField(blank=True, default={}),
        ),
    ]
