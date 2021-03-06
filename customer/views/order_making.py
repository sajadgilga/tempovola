import datetime
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from persiandate import jalali
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from customer.models import CustomerProfile, Melody, Order, ShopItem, Promotions, Series
from customer.serializers import CustomerSerializer


def get_new_order_id():
    last_order_made = Order.objects.filter(is_checked_out=True).last()
    last_id = '000001'
    if last_order_made and last_order_made.order_id:
        last_id = str(int(last_order_made.order_id.split('W')[1]) + 1)
        if len(last_id) < 6:
            last_id = '0' * (6 - len(last_id)) + last_id
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    currentDate = jalali.Gregorian(date).persian_string().split('-')[0]
    id = str(currentDate) + 'W' + last_id
    return id


def check_promotion(promotion, order, total_count):
    is_promoted = True
    for scenario in promotion.scenarios.all():
        if scenario.total_count != 0:
            if not scenario.total_count <= total_count:
                is_promoted = False
                break
        elif scenario.items != '':
            for item in scenario.items.split('--'):
                if not ShopItem.objects.filter(
                        order=order,
                        series=item.split('..')[0],
                        melody_name=item.split('..')[1]
                ).exists():
                    is_promoted = False
                    break
        elif scenario.series_items != '':
            for item in scenario.items.split('--'):
                if not ShopItem.objects.filter(
                        order=order,
                        series=item
                ).exists():
                    is_promoted = False
                    break
        elif scenario.melody_items != '':
            for item in scenario.items.split('--'):
                if not ShopItem.objects.filter(
                        order=order,
                        melody_name=item
                ).exists():
                    is_promoted = False
                    break
        return is_promoted


def apply_promotions(order, total_count):
    promotions = Promotions.objects.filter(active=True).all()
    discount_percent = 0
    for promotion in promotions:
        if check_promotion(promotion, order, total_count):
            discount_percent += promotion.discount_percent
    return discount_percent


@api_view(['GET', 'POST'])
@login_required(login_url='/')
def enter_shop(request, series=''):
    user = request.user
    try:
        customer = CustomerProfile.objects.get(user=user)

        context = {'name': customer.company_name, 'vis_series': series}
        return render(request, 'customer/shop.html', context)
    except:
        return render(request, 'customer/login.html')


def find_melody(melodies, product, melody):
    for m in melodies:
        if m.melody_name == melody['name'] and m.series == product['name']:
            return m
    return None


@api_view(['GET', 'POST'])
@login_required(login_url='/')
def fetch_data(request):
    user = request.user
    # try:
    customer = CustomerProfile.objects.get(user=user)
    context = CustomerSerializer(customer)
    context = context.data
    context = json.loads(JSONRenderer().render(context))

    order = Order.objects.filter(customer=CustomerProfile.objects.get(user=user)).all().last()
    if order and not order.is_checked_out:
        items = ShopItem.objects.filter(order=order)
        for product in context['available_series']:
            cost = 0
            for melody in product['melodies']:
                m = find_melody(items, product, melody)
                if m:
                    melody['count'] = m.ordered_count
                    cost += product['price'] * melody['count']
            product['total_cost'] = cost

    promotions = Promotions.objects.filter(active=True).all()
    promotion_json = []
    for p in promotions:
        promotion_json.append({
            "description": p.description,
            "url": p.img.storage.base_location + '/' + p.img.name
        })
    context["promotions"] = promotion_json
    return Response(context)
    # except:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)


# for checking out order, this order now becomes available to admins and will be processed later
@api_view(['POST'])
@login_required(login_url='/')
def checkout(request):
    user = request.user
    data = request.data['list']
    cost = 0
    customer = CustomerProfile.objects.get(user=user)
    order = Order.objects.filter(customer=customer).all().last()
    total_count = 0
    if not order or order.is_checked_out:
        order = Order(customer_id=customer.pk)
        order.save()
    else:
        ShopItem.objects.filter(order=order).all().delete()
    for p in data:
        for m in data[p]:
            price = Series.objects.filter(name=p)[0].price
            cost += int(data[p][m]) * int(price)
            melody = ShopItem.objects.filter(melody_name=m, order=order, series=p).all().first()
            total_count += int(data[p][m])
            if melody:
                melody.ordered_count = int(data[p][m])
                melody.order_admin_verified_count = int(data[p][m])
                melody.save(force_update=True)
            else:
                new_melody = ShopItem(melody_name=m, order=order,
                                      series=p, price=int(price),
                                      ordered_count=int(data[p][m]),
                                      order_admin_verified_count=int(data[p][m])
                                      )
                new_melody.save(force_insert=True)
    order.cost = cost
    order.order_id = get_new_order_id()
    order.save()
    discount_percent = apply_promotions(order, total_count)
    order.discount = discount_percent
    order.save()
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
@login_required(login_url='/')
def get_music(request):
    mel = Melody.objects.filter(name=request.data['melody']).all().first()
    return Response(mel.music.storage.base_location + '/' + mel.music.name)
