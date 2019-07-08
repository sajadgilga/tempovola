# Generated by Django 2.2 on 2019-07-06 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotionScenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_count', models.IntegerField(default=0)),
                ('items', models.CharField(blank=True, max_length=2048)),
                ('series_items', models.CharField(blank=True, max_length=1024)),
                ('melody_items', models.CharField(blank=True, max_length=2048)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='promotions',
            name='scenarios',
            field=models.ManyToManyField(to='customer.PromotionScenario'),
        ),
    ]
