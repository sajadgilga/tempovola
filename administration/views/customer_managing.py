import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from persiandate import jalali
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from customer.models import Order, ShopItem, SchemaSeries, CustomerProfile, Series, Melody

admins = ['admin', 'orderAdmin', 'sellAdmin', 'warehouseAdmin']


def check_access(user):
    if user.groups.filter(name__in=admins):
        return True
    else:
        return False


def get_new_customer_id():
    last_customer_made = CustomerProfile.objects.all().last()
    id_num = '00001'
    if last_customer_made.customer_id:
        id_num = str(int(last_customer_made.customer_id.split('C')[1]) + 1)
        if len(id_num) < 6:
            id_num = '0' * (6 - len(id_num)) + id_num
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    currentDate = jalali.Gregorian(date).persian_string().split('-')[0]
    id = str(currentDate) + 'C' + id_num
    return id


@api_view(['GET'])
@login_required(login_url='/admin/')
def enter_dashboard(request):
    try:
        user = request.user
        if not check_access(user):
            return Response({'msg': 'سطح دسترسی لازم را ندارید'}, status=status.HTTP_401_UNAUTHORIZED)
        new_orders = len(Order.objects.filter(is_confirmed=False).all())
        return render(request, 'admin/admin_dashboard.html', {'newOrders': new_orders, 'name': user.username})
    except:
        return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@login_required(login_url='/admin/')
def profile_maker(request):
    try:
        user = request.user
        return render(request, 'admin/profile_maker.html', {'name': user.username})
    except:
        return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@login_required(login_url='/admin/')
def get_products(request):
    try:
        products = SchemaSeries.objects.all().values_list('name', 'melodies__name')
        return Response({'products': products}, status=status.HTTP_200_OK)
    except:
        return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@login_required(login_url='/admin/')
def signup_customer(request):
    # try:
    form = request.data['form']

    if CustomerProfile.objects.filter(email=form['email']).exists():
        return Response({'msg': 'ایمیل مورد نظر قبلا در سامانه ثبت شده است'},
                        status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=form[form['username_type'][0]]).exists():
        return Response({'msg': 'ایمیل مورد نظر قبلا در سامانه ثبت شده است'},
                        status=status.HTTP_400_BAD_REQUEST)

    if 'phone' in form['username_type']:
        if CustomerProfile.objects.filter(phone=form['phone']).exists():
            return Response({'msg': 'شماره تماس مورد نظر قبلا در سامانه ثبت شده است'},
                            status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=form[form['username_type'][0]],
                                    email=form['email'], password=form['password'])
    customer = CustomerProfile()
    customer.user = user
    customer.email = form['email']
    customer.phone = form['phone']
    customer.company_name = form['company_name']
    customer.city = form['city']
    customer.address = form['address']
    customer.customer_id = get_new_customer_id()
    customer.save()

    for product in form['available_series']:
        schema_series = SchemaSeries.objects.filter(name=product)[0]
        series = Series()
        series.name = schema_series.name
        series.product_code = schema_series.product_code
        series.description = schema_series.description
        series.picture = schema_series.picture
        series.save()
        for mel_name in form['melodies'][product]:
            mel_schema = schema_series.melodies.get(name=mel_name)
            melody = Melody()
            melody.name = mel_name
            melody.melody_code = mel_schema.melody_code
            melody.price = mel_schema.price
            melody.save()
            series.melodies.add(melody)
        series.save()
        customer.available_series.add(series)
    customer.save()
    return Response(status=status.HTTP_200_OK)
    # except:
    #     return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@login_required(login_url='/admin/')
def product_maker(request):
    try:
        user = request.user
        return render(request, 'admin/product_maker.html', {'name': user.username})
    except:
        return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

