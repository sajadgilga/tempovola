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
    operator_name = models.CharField(db_index=True, max_length=64)
    company_name = models.CharField(db_index=True, max_length=86)
    customer_id = models.CharField(db_index=True, max_length=32, default='')
    email = models.EmailField(blank=True)
    phone = PhoneField(blank=True, help_text='contact phone number')
    city = models.CharField(max_length=128, default='')
    state = models.CharField(max_length=128, default='')
    address = models.CharField(max_length=256, default='')
    # TODO: set default available series
    available_series = models.ManyToManyField('Series')


class SchemaSeries(models.Model):
    name = models.CharField(max_length=24, db_index=True)
    product_code = models.CharField(db_index=True, max_length=32, default='')
    description = models.CharField(max_length=128, blank=True)
    melodies = models.ManyToManyField('Melody')
    price = models.IntegerField(default=0)
    picture = models.FileField(storage=imageFS, null=True)


class Series(models.Model):
    name = models.CharField(max_length=24, db_index=True)
    product_code = models.CharField(db_index=True, max_length=32, default='')
    description = models.CharField(max_length=128, blank=True)
    total_cost = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    melodies = models.ManyToManyField('Melody')
    price = models.IntegerField(default=0)
    picture = models.FileField(storage=imageFS, null=True)


class Melody(models.Model):
    name = models.CharField(max_length=32, db_index=True)
    melody_code = models.CharField(max_length=32, db_index=True, default='')
    music = models.FileField(storage=audioFS, null=True)
    picture = models.FileField(storage=imageFS, null=True)


class Order(models.Model):
    customer = models.ForeignKey(to='CustomerProfile', on_delete=models.CASCADE, related_name='customer')
    order_id = models.CharField(max_length=32, db_index=True, default='')
    is_checked_out = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    # is_received = models.BooleanField(default=False)
    # received_date = models.DateTimeField(blank=True, null=True)
    CHECKED_OUT = 0
    ORDER_ADMIN = 1
    SELL_ADMIN = 2
    WAREHOUSE_ADMIN = 3
    FINANCE_ADMIN = 4
    ADMINISTRATION = 5
    CONFIRMED = 6
    SENT = 7
    STATUS = (
        (-1, 'created'),
        (CHECKED_OUT, 'checked_out'),
        (ORDER_ADMIN, 'orderAdmin_confirmed'),
        (SELL_ADMIN, 'sellAdmin_confirmed'),
        (WAREHOUSE_ADMIN, 'warehouseAdmin_confirmed'),
        (FINANCE_ADMIN, 'financeAdmin_confirmed'),
        (ADMINISTRATION, 'administration_process'),
        (CONFIRMED, 'confirmed'),
        (SENT, 'sent')
    )
    status = models.CharField(default=-1, choices=STATUS, max_length=128)
    # orderAdmin_confirmed = models.BooleanField(default=False)
    # sellAdmin_confirmed = models.BooleanField(default=False)
    # warehouseAdmin_confirmed = models.BooleanField(default=False)
    # financeAdmin_confirmed = models.BooleanField(default=False)
    # administration_process = models.BooleanField(default=False)

    orderAdmin_comment = models.CharField(max_length=256, default='')
    sellAdmin_comment = models.CharField(max_length=256, default='')
    warehouseAdmin_comment = models.CharField(max_length=256, default='')
    financeAdmin_comment = models.CharField(max_length=256, default='')
    administration_comment = models.CharField(max_length=256, default='')

    last_change_date = models.DateTimeField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    confirmed_date = models.DateTimeField(blank=True, null=True)
    sent_date = models.DateTimeField(blank=True, null=True)
    cost = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)


class ShopItem(models.Model):
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    series = models.CharField(max_length=25, db_index=True)
    order = models.ForeignKey(to='Order', on_delete=models.CASCADE, related_name='items')
    melody_name = models.CharField(max_length=32, db_index=True)
    price = models.IntegerField(default=0)
    ordered_count = models.IntegerField(default=0)
    order_admin_verified_count = models.IntegerField(default=0)
    sell_admin_verified_count = models.IntegerField(default=0)


class Promotions(models.Model):
    description = models.CharField(max_length=256, db_index=True)
    scenarios = models.ManyToManyField(to='PromotionScenario')
    img = models.FileField(storage=imageFS)
    active = models.BooleanField(default=True)
    discount_percent = models.IntegerField(default=0)


class PromotionScenario(models.Model):
    total_count = models.IntegerField(default=0)
    items = models.CharField(max_length=2048, blank=True)
    series_items = models.CharField(max_length=1024, blank=True)
    melody_items = models.CharField(max_length=2048, blank=True)


class Report(models.Model):
    owner = models.ForeignKey(to='CustomerProfile', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.CharField(max_length=512)
    answer = models.CharField(max_length=512, default='')
    is_active = models.BooleanField(default=True)
