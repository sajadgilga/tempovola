# Generated by Django 2.2 on 2019-11-29 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0016_auto_20191129_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
