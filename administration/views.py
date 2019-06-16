import datetime
import json

import xlwt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from kavenegar import *
from persiandate import jalali
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from customer.models import Order, ShopItem, ProductSeries, CustomerProfile
from customer.serializers import OrderSerializer


def check_access(user):
    if user.groups.filter(name__in=['admin', ]):
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
def enter_admin_login(request):
    return render(request, 'admin/adminlogin.html')


@api_view(['POST'])
def login_(request):
    # try:
    body = request.body
    user_data = json.loads(body)
    # api = KavenegarAPI('6652373751486A6D5A34584B476A466F346E616F7A313768553441726330554E')
    # params = {'sender': '1000596446', 'receptor': '09366637984', 'message': "با موفقیت تست شد".encode('utf-8')}
    # response = api.sms_send(params)
    user = authenticate(request, username=user_data['username'], password=user_data['password'])
    if user is None:
        return Response({'msg': 'اطلاعات وارد شده غلط می‌باشد. دوباره تلاش کنید'},
                        status=status.HTTP_401_UNAUTHORIZED)
    if not user.groups.filter(name__in=['admin']).exists():
        return Response({'msg': 'سطح دسترسی لازم را ندارید'}, status=status.HTTP_401_UNAUTHORIZED)

    login(request, user)
    return Response({'msg': 'login successful'}, status=status.HTTP_200_OK)
    # except:
    #     return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def logout_(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


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
        products = ProductSeries.objects.all().values_list('name')
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
        customer.available_series.add(ProductSeries.objects.filter(name=product[0])[0])
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


@api_view(['GET'])
@login_required(login_url='/admin/')
def get_order_list(request):
    try:
        user = request.user
        return render(request, 'admin/order_list.html', {'name': user.username})
    except:
        return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@login_required(login_url='/admin/')
def get_orders(request):
    try:
        user = request.user
        orders = Order.objects.all().order_by('created_date')
        orders = OrderSerializer(orders, many=True).data
        orders = json.loads(JSONRenderer().render(orders))
        for order in orders:
            order['created_date'] = jalali.Gregorian(order['created_date'].split('T')[0]).persian_string()
        return Response({'orders': orders})
    except:
        return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@login_required(login_url='/admin/')
def get_order_excel(request):
    # try:
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="orders.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('گزارشات')

    ws.cols_right_to_left = 1
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        'نام خریدار',
        'کد سفارش',
        'استان',
        'شهر',
        'آدرس خریدار',
        'قیمت',
        'تاریخ سفارش',
        'تاریخ تغییر',
        'تاریخ تایید',
        'تاریخ ارسال',
        'تاریخ تحویل',
        'وضعیت',
    ]

    row_name = 0

    for col in range(len(columns)):
        ws.write(row_name, col, columns[col], font_style)

    font_style = xlwt.XFStyle()

    orders = Order.objects.filter(is_checked_out=True).all().order_by('-created_date')
    for order in orders:
        row_name += 1
        ws.write(row_name, 0, order.customer.company_name, font_style)
        ws.write(row_name, 1, order.order_id, font_style)
        ws.write(row_name, 2, '', font_style)  # TODO add state
        ws.write(row_name, 3, order.customer.city, font_style)
        ws.write(row_name, 4, order.customer.address, font_style)
        ws.write(row_name, 5, order.cost, font_style)
        ws.write(row_name, 6, jalali.Gregorian(order.created_date.strftime('%Y-%m-%d')).persian_string(),
                 font_style)
        if order.last_change_date:
            ws.write(row_name, 7, jalali.Gregorian(order.last_change_date.strftime('%Y-%m-%d')).persian_string(),
                     font_style)
        if order.confirmed_date:
            ws.write(row_name,8, jalali.Gregorian(order.confirmed_date.strftime('%Y-%m-%d')).persian_string(),
                     font_style)
        if order.sent_date:
            ws.write(row_name, 9, jalali.Gregorian(order.sent_date.strftime('%Y-%m-%d')).persian_string(),
                     font_style)
        if order.received_date:
            ws.write(row_name, 10, jalali.Gregorian(order.received_date.strftime('%Y-%m-%d')).persian_string(),
                     font_style)
        if order.is_received:
            ws.write(row_name, 11, 'تحویل شده',
                     font_style)
        elif order.is_confirmed:
            ws.write(row_name, 11, 'تایید شده',
                     font_style)
        else:
            ws.write(row_name,11, 'تایید نشده',
                     font_style)

    wb.save(response)
    return response
    # except:
    #     return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
