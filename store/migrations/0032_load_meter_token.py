# Generated by Django 2.2.5 on 2020-05-15 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_auto_20200425_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='load_meter',
            name='token',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]