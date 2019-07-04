import uuid

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.
from phone_field import PhoneField

audioFS = FileSystemStorage(location='media/melodies')
imageFS = FileSystemStorage(location='media/images')


class CustomerProfile(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    company_name = models.CharField(db_index=True, max_length=64)
    customer_id = models.CharField(db_index=True, max_length=32, default='')
    email = models.EmailField(blank=True)
    phone = PhoneField(blank=True, help_text='contact phone number')
    city = models.CharField(max_length=128, default='')
    address = models.CharField(max_length=256, default='')
    # TODO: set default available series
    available_series = models.ManyToManyField('Series')


class SchemaSeries(models.Model):
    name = models.CharField(max_length=24, db_index=True)
    product_code = models.CharField(db_index=True, max_length=32, default='')
    description = models.CharField(max_length=128, blank=True)
    melodies = models.ManyToManyField('Melody')
    picture = models.FileField(storage=imageFS, null=True)


class Series(models.Model):
    name = models.CharField(max_length=24, db_index=True)
    product_code = models.CharField(db_index=True, max_length=32, default='')
    description = models.CharField(max_length=128, blank=True)
    total_cost = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    melodies = models.ManyToManyField('Melody')
    picture = models.FileField(storage=imageFS, null=True)


class Melody(models.Model):
    name = models.CharField(max_length=32, db_index=True)
    melody_code = models.CharField(max_length=32, db_index=True, default='')
    price = models.IntegerField(default=3000)
    count = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    # TODO: (*Phase_2) handle music properly
    music = models.FileField(storage=audioFS, null=True)


class Order(models.Model):
    customer = models.ForeignKey(to='CustomerProfile', on_delete=models.CASCADE, related_name='customer')
    order_id = models.CharField(max_length=32, db_index=True, default='')
    is_checked_out = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)
    orderAdmin_confirmed = models.BooleanField(default=False)
    sellAdmin_confirmed = models.BooleanField(default=False)
    warehouseAdmin_confirmed = models.BooleanField(default=False)
    financeAdmin_confirmed = models.BooleanField(default=False)
    last_change_date = models.DateTimeField(blank=True, null=True)
    confirmed_date = models.DateTimeField(blank=True, null=True)
    sent_date = models.DateTimeField(blank=True, null=True)
    received_date = models.DateTimeField(blank=True, null=True)
    cost = models.IntegerField(default=0)


class ShopItem(models.Model):
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    series = models.CharField(max_length=25, db_index=True)
    order = models.ForeignKey(to='Order', on_delete=models.CASCADE, related_name='order')
    melody_name = models.CharField(max_length=32, db_index=True)
    price = models.IntegerField(default=0)
    count = models.IntegerField(default=0)


class Promotions(models.Model):
    description = models.CharField(max_length=256, db_index=True)
    img = models.FileField(storage=imageFS)
    active = models.BooleanField(default=True)
