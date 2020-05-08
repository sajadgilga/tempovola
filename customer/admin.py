from django.contrib import admin

# Register your models here.
from customer.models import CustomerProfile, SchemaSeries, Melody, Order, ShopItem, Series, Promotions, Report, \
    PromotionScenario


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
                    'is_confirmed', 'order_id',
                    'created_date', 'last_change_date',
                    'confirmed_date', 'sent_date',
                    'status')


@admin.register(ShopItem)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('series', 'order',
                    'melody_name', 'price',
                    'ordered_count', 'order_admin_verified_count',
                    'sell_admin_verified_count',)


@admin.register(Promotions)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('description',)


@admin.register(PromotionScenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('total_count', 'items', 'series_items', 'melody_items')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('owner', 'date', 'description',)
    search_fields = ('owner',)
    list_filter = ('owner',)
