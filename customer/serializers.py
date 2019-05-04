from rest_framework import serializers

from customer.models import CustomerProfile, ProductSeries, Melody, Order, ShopItem


class MelodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Melody
        fields = ('name', 'price', 'count', 'melody_code')


class ProductSerializer(serializers.ModelSerializer):
    melodies = MelodySerializer(many=True)

    class Meta:
        model = ProductSeries
        fields = ('name', 'description', 'melodies',
                  'total_cost', 'product_code')


class CustomerSerializer(serializers.ModelSerializer):
    available_series = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ('company_name', 'email', 'phone', 'address',
                  'available_series', 'city', 'customer_id')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopItem
        fields = ('series',
                  'melody_name', 'price',
                  'count', )


class OrderSerializer(serializers.ModelSerializer):
    # items = ItemSerializer(many=True)
    # customer = serializers.CharField(source='customer.company_name')

    class Meta:
        model = Order
        fields = (
                  'is_confirmed', 'is_received',
                  'created_date', 'last_change_date',
                  'confirmed_date', 'sent_date',
                  'received_date', 'cost', 'order_id')

