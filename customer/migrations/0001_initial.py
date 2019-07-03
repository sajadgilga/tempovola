# Generated by Django 2.2 on 2019-07-03 16:30

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(db_index=True, max_length=64)),
                ('customer_id', models.CharField(db_index=True, default='', max_length=32)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', phone_field.models.PhoneField(blank=True, help_text='contact phone number', max_length=31)),
                ('city', models.CharField(default='', max_length=128)),
                ('address', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Melody',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=32)),
                ('melody_code', models.CharField(db_index=True, default='', max_length=32)),
                ('price', models.IntegerField(default=3000)),
                ('count', models.IntegerField(default=0)),
                ('discount', models.IntegerField(default=0)),
                ('music', models.FileField(null=True, storage=django.core.files.storage.FileSystemStorage(location='media/melodies'), upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(db_index=True, default='', max_length=32)),
                ('is_checked_out', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('is_received', models.BooleanField(default=False)),
                ('last_change_date', models.DateTimeField(blank=True, null=True)),
                ('confirmed_date', models.DateTimeField(blank=True, null=True)),
                ('sent_date', models.DateTimeField(blank=True, null=True)),
                ('received_date', models.DateTimeField(blank=True, null=True)),
                ('cost', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='customer.CustomerProfile')),
            ],
        ),
        migrations.CreateModel(
            name='ShopItem',
            fields=[
                ('item_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('series', models.CharField(db_index=True, max_length=25)),
                ('melody_name', models.CharField(db_index=True, max_length=32)),
                ('price', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='customer.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=24)),
                ('product_code', models.CharField(db_index=True, default='', max_length=32)),
                ('description', models.CharField(blank=True, max_length=128)),
                ('total_cost', models.IntegerField(default=0)),
                ('discount', models.IntegerField(default=0)),
                ('picture', models.FileField(null=True, storage=django.core.files.storage.FileSystemStorage(location='media/melodies'), upload_to='')),
                ('melodies', models.ManyToManyField(to='customer.Melody')),
            ],
        ),
        migrations.CreateModel(
            name='SchemaSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=24)),
                ('product_code', models.CharField(db_index=True, default='', max_length=32)),
                ('description', models.CharField(blank=True, max_length=128)),
                ('total_cost', models.IntegerField(default=0)),
                ('picture', models.FileField(null=True, storage=django.core.files.storage.FileSystemStorage(location='media/melodies'), upload_to='')),
                ('melodies', models.ManyToManyField(to='customer.Melody')),
            ],
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='available_series',
            field=models.ManyToManyField(to='customer.SchemaSeries'),
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
