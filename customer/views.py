import io
import json

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from weasyprint import HTML

from customer.models import CustomerProfile, Melody, Order, ShopItem
from customer.serializers import CustomerSerializer, OrderSerializer, ItemSerializer


@api_view(['GET'])
def enter_home(request):
    return render(request, 'customer/login.html')


@api_view(['POST'])
def login_(request):
    if request.method != 'POST':
        return Response({'msg': 'You must use POST method to send request'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        body = request.body
        user_data = json.loads(body)
        user = authenticate(request, username=user_data['username'], password=user_data['password'])
        if user is None:
            return Response({'msg': 'اطلاعات وارد شده غلط می‌باشد. دوباره تلاش کنید'},
                            status=status.HTTP_401_UNAUTHORIZED)
        if len(CustomerProfile.objects.filter(user=user)) is 0:
            return Response({'msg': 'این پروفایل در سامانه ثبت نشده. به پشتیبانی اطلاع دهید'},
                            status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        return Response({'msg': 'login successful'}, status=status.HTTP_200_OK)
    except:
        return Response({'msg': 'مشکلی در سرور به وجود آمذه'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def logout_(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@login_required(login_url='/')
def enter_shop(request):
    user = request.user
    try:
        customer = CustomerProfile.objects.get(user=user)

        context = {'name': customer.company_name}
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
    try:
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
                        melody['count'] = m.count
                        cost += melody['price'] * melody['count']
                product['total_cost'] = cost

        return Response(context)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_required(login_url='/')
def profile(request):
    try:
        user = request.user
        customer = CustomerProfile.objects.filter(user=user)[0]
        context = CustomerSerializer(customer)
        context = json.loads(JSONRenderer().render(context.data))
        return render(request, 'customer/profile.html', {'name': customer.company_name, 'context': context})
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@login_required(login_url='/')
def checkout(request):
    user = request.user
    data = request.data['list']
    cost = 0
    customer = CustomerProfile.objects.get(user=user)
    order = Order.objects.filter(customer=customer).all().last()
    if not order or order.is_checked_out:
        order = Order(customer_id=customer.pk)
        order.save()
    for p in data:
        for m in data[p]:
            price = Melody.objects.filter(name=m)[0].price
            cost += int(data[p][m]) * int(price)
            melody = ShopItem.objects.filter(melody_name=m, order=order, series=p).all().first()
            if melody:
                melody.count = int(data[p][m])
                melody.save(force_update=True)
            else:
                new_melody = ShopItem(melody_name=m, order=order, series=p, price=int(price), count=int(data[p][m]))
                new_melody.save(force_insert=True)
    order.cost = cost
    order.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@login_required(login_url='/')
def enter_checkout(request):
    try:
        return render(request, 'customer/checkout.html')
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@login_required(login_url='/')
def get_checkout_data(request):
    try:
        user = request.user
        order = Order.objects.filter(customer=CustomerProfile.objects.get(user=user)).all().last()
        context = OrderSerializer(order).data
        context = json.loads(JSONRenderer().render(context))
        items = ShopItem.objects.filter(order=order)
        items = ItemSerializer(items, many=True)
        items = JSONRenderer().render(items.data)
        items = json.loads(items)
        context['items'] = items
        context['name'] = order.customer.company_name
        return Response(context, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@login_required(login_url='/')
def confirm_checkout(request):
    try:
        user = request.user
        order = Order.objects.filter(customer=CustomerProfile.objects.get(user=user)).all().last()
        order.is_checked_out = True
        order.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@login_required(login_url='/')
def enter_confirm_checkout(request):
    return render(request, 'customer/confirm_receipt.html')


@api_view(['GET'])
@login_required(login_url='/')
def get_receipt(request):
    user = request.user
    order = Order.objects.filter(customer=CustomerProfile.objects.get(user=user)).all().last()
    items = ShopItem.objects.filter(order=order)
    items = ItemSerializer(items, many=True)
    items = JSONRenderer().render(items.data)
    items = json.loads(items)
    html_string = render_to_string('customer/receipt.html', {'items': items})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response
    return response
