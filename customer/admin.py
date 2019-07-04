from django.contrib import admin

# Register your models here.
from customer.models import CustomerProfile, SchemaSeries, Melody, Order, ShopItem, Series, Promotions


@admin.register(CustomerProfile)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name',
                    'phone', 'email',
                    'address', 'city', 'customer_id')
    search_fields = ('user', 'company_name',
                     'phone', 'email',
                     'address', 'city', 'customer_id')
    list_filter = ('user', 'company_name',
                   'phone', 'email',
                   'address', 'city')


@admin.register(SchemaSeries)
class ProductSeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'product_code', 'picture')


@admin.register(Series)
class ProductSeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'product_code', 'picture')


@admin.register(Melody)
class MelodyAdmin(admin.ModelAdmin):
    list_display = ('name', 'music', 'melody_code')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'cost', 'is_checked_out',
                    'is_confirmed', 'is_received', 'order_id',
                    'created_date', 'last_change_date',
                    'confirmed_date', 'sent_date', 'received_date')


@admin.register(ShopItem)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('series', 'order',
                    'melody_name', 'price', 'count')


@admin.register(Promotions)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('description', )
