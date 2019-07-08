from rest_framework import serializers

from customer.models import CustomerProfile, SchemaSeries, Melody, Order, ShopItem, Series


class MelodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Melody
        fields = ('name', 'price', 'count', 'melody_code')


class ProductSerializer(serializers.ModelSerializer):
    melodies = MelodySerializer(many=True)

    class Meta:
        model = Series
        fields = ('name', 'description', 'melodies',
                  'total_cost', 'product_code')


class CustomerSerializer(serializers.ModelSerializer):
    available_series = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ('company_name', 'email', 'phone', 'address',
                  'available_series', 'city', 'customer_id')


class CustomerOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerProfile
        fields = ('company_name', 'email', 'phone', 'address',
                  'city',)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopItem
        fields = ('series',
                  'melody_name', 'price',
                  'ordered_count', 'order_admin_verified_count',
                  'sell_admin_verified_count',)


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    customer = CustomerOrderSerializer()

    class Meta:
        model = Order
        fields = ('customer', 'discount', 'items',
                  'is_confirmed', 'is_received',
                  'created_date', 'last_change_date',
                  'confirmed_date', 'sent_date',
                  'received_date', 'cost', 'order_id',
                  'orderAdmin_confirmed', 'sellAdmin_confirmed',
                  'warehouseAdmin_confirmed', 'financeAdmin_confirmed',
                  'administration_process'
                  )

