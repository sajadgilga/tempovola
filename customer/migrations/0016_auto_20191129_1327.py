# Generated by Django 2.2 on 2019-11-29 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0015_auto_20191129_1235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_received',
        ),
        migrations.RemoveField(
            model_name='order',
            name='received_date',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(-1, 'created'), (0, 'checked_out'), (1, 'orderAdmin_confirmed'), (2, 'sellAdmin_confirmed'), (3, 'warehouseAdmin_confirmed'), (4, 'financeAdmin_confirmed'), (5, 'administration_process'), (6, 'confirmed'), (7, 'sent')], default=-1, max_length=128),
        ),
    ]
