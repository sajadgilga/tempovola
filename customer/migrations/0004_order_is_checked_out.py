# Generated by Django 2.2 on 2019-04-25 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20190424_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_checked_out',
            field=models.BooleanField(default=False),
        ),
    ]