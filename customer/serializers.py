from rest_framework import serializers

from customer.models import CustomerProfile, SchemaSeries, Melody, Order, ShopItem, Series, Report


class MelodySerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = Melody
        fields = ('name', 'melody_code', 'img')

    def get_img(self, obj):
        if not obj.picture:
            return ''
        return obj.picture.storage.base_location + '/' + obj.picture.name


class ProductSerializer(serializers.ModelSerializer):
    melodies = MelodySerializer(many=True)
    picture = serializers.SerializerMethodField()

    class Meta:
        model = Series
        fields = ('name', 'description', 'melodies', 'price',
                  'total_cost', 'product_code', 'picture')

    def get_picture(self, obj):
        if not obj.picture:
            return ''
        return obj.picture.storage.base_location + '/' + obj.picture.name


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
                  'is_confirmed',
                  'created_date', 'last_change_date',
                  'confirmed_date', 'sent_date',
                  'cost', 'order_id',
                  'status', 'orderAdmin_comment',
                  'sellAdmin_comment', 'warehouseAdmin_comment',
                  'financeAdmin_comment', 'administration_comment'
                  )


class ReportSerializer(serializers.ModelSerializer):
    owner = CustomerOrderSerializer()

    class Meta:
        model = Report
        fields = ('owner', 'date', 'description', 'answer', 'is_active')
