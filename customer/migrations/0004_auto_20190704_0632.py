# Generated by Django 2.2 on 2019-07-04 06:32

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20190703_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(db_index=True, max_length=256)),
                ('img', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='media/images'), upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='schemaseries',
            name='picture',
            field=models.FileField(null=True, storage=django.core.files.storage.FileSystemStorage(location='media/images'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='series',
            name='picture',
            field=models.FileField(null=True, storage=django.core.files.storage.FileSystemStorage(location='media/images'), upload_to=''),
        ),
    ]
