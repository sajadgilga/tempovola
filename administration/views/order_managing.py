import json

import xlwt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from persiandate import jalali
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from customer.models import Order
from customer.serializers import OrderSerializer

admins = ['admin', 'orderAdmin', 'sellAdmin', 'warehouseAdmin']


def check_access(user):
    if user.groups.filter(name__in=admins):
        return True
    else:
        return False


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
        if user.groups.filter(name__in=[admins[1], ]).exists():
            orders = Order.objects.filter(orderAdmin_confirmed=False, is_confirmed=True)\
                .all().order_by('created_date')
        elif user.groups.filter(name__in=[admins[2], ]):
            orders = Order.objects.filter(orderAdmin_confirmed=True, sellAdmin_confirmed=False)\
                .all().order_by('created_date')
        elif user.groups.filter(name__in=[admins[3], ]):
            orders = Order.objects.filter(sellAdmin_confirmed=True, orderAdmin_confirmed=False)\
                .all().order_by('created_date')
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
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
            ws.write(row_name, 8, jalali.Gregorian(order.confirmed_date.strftime('%Y-%m-%d')).persian_string(),
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
            ws.write(row_name, 11, 'تایید نشده',
                     font_style)

    wb.save(response)
    return response
    # except:
    #     return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
