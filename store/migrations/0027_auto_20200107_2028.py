# Generated by Django 2.2.5 on 2020-01-07 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_auto_20200107_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_consumption',
            name='day',
            field=models.CharField(max_length=20),
        ),
    ]