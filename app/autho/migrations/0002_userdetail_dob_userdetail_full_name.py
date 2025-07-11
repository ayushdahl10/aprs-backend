# Generated by Django 4.2.3 on 2023-12-23 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autho', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='dob',
            field=models.DateField(help_text='Enter date of birth', null=True),
        ),
        migrations.AddField(
            model_name='userdetail',
            name='full_name',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]
