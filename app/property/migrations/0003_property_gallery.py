# Generated by Django 4.2.3 on 2023-12-23 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_property_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='gallery',
            field=models.ImageField(blank=True, null=True, upload_to='image/property/'),
        ),
    ]
