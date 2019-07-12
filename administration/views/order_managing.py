import datetime
import json

import xlwt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from kavenegar import KavenegarAPI
from persiandate import jalali
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from TempoVola.settings import admins
from customer.models import Order, ShopItem
from customer.serializers import OrderSerializer


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
        if user.groups.filter(name__in=[admins[1], ]).exists():
            return render(request, 'admin/order_list.html', {'name': user.username})
        elif user.groups.filter(name__in=[admins[2], ]).exists():
            return render(request, 'admin/sellAdmin_list.html', {'name': user.username})
        elif user.groups.filter(name__in=[admins[3], ]).exists():
            return render(request, 'admin/warehouseAdmin_list.html', {'name': user.username})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@login_required(login_url='/admin/')
def get_orders(request):
    # try:
    user = request.user
    if user.groups.filter(name__in=[admins[1], ]).exists():
        orders = Order.objects.filter(orderAdmin_confirmed=False, is_checked_out=True,
                                      administration_process=False) \
            .all().order_by('-created_date')
    elif user.groups.filter(name__in=[admins[2], ]).exists():
        orders = Order.objects.filter(orderAdmin_confirmed=True, sellAdmin_confirmed=False,
                                      administration_process=False) \
            .all().order_by('-created_date')
    elif user.groups.filter(name__in=[admins[3], ]).exists():
        orders = Order.objects.filter(sellAdmin_confirmed=True, warehouseAdmin_confirmed=False,
                                      administration_process=False) \
            .all().order_by('-created_date')
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    orders = OrderSerializer(orders, many=True)
    orders = json.loads(JSONRenderer().render(orders.data))
    for order in orders:
        order['created_date'] = jalali.Gregorian(order['created_date'].split('T')[0]).persian_string()
    return Response({'orders': orders})
    # except:
    #     return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def send_verification_sms(phone, message):
    api = KavenegarAPI('6652373751486A6D5A34584B476A466F346E616F7A313768553441726330554E')
    params = {
        'sender': '1000596446',
        'receptor': phone,
        'message': message.encode('utf-8')
    }
    try:
        response = api.sms_send(params)
    except:
        print("شماره کاربر مشکل دارد")


@api_view(['POST'])
@login_required(login_url='/admin/')
def verify_order(request):
    user = request.user
    if user.groups.filter(name__in=[admins[1], ]).exists():
        admin_verified_order = request.data['order']
        order = Order.objects.filter(order_id=admin_verified_order['order_id'],
                                     orderAdmin_confirmed=False).all().first()
        order.last_change_date = timezone.now()
        order.orderAdmin_confirmed = True
        order.cost = admin_verified_order['cost']
        saved_items = ShopItem.objects.filter(order=order).all()
        if len(saved_items) != len(admin_verified_order['items']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for index, item in enumerate(admin_verified_order['items']):
            saved_items[index].order_admin_verified_count = int(item['order_admin_verified_count'])
            saved_items[index].sell_admin_verified_count = int(item['order_admin_verified_count'])
            saved_items[index].save()
        order.save()
        send_verification_sms(order.customer.phone, "کاربر گرامی، سفارش شما از مرحله سفارش با موفقیت عبور کرد")
    elif user.groups.filter(name__in=[admins[2], ]).exists():
        admin_verified_order = request.data['order']
        order = Order.objects.filter(order_id=admin_verified_order['order_id'],
                                     sellAdmin_confirmed=False).all().first()
        order.last_change_date = timezone.now()
        order.sellAdmin_confirmed = True
        order.cost = admin_verified_order['cost']
        saved_items = ShopItem.objects.filter(order=order).all()
        if len(saved_items) != len(admin_verified_order['items']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for index, item in enumerate(admin_verified_order['items']):
            saved_items[index].sell_admin_verified_count = item['sell_admin_verified_count']
            saved_items[index].warehouse_admin_verified_count = item['sell_admin_verified_count']
            saved_items[index].save()
        order.save()
        send_verification_sms(order.customer.phone, "کاربر گرامی، سفارش شما از مرحله فروش با موفقیت عبور کرد")
    elif user.groups.filter(name__in=[admins[3], ]).exists():
        admin_verified_order = request.data['order']
        order = Order.objects.filter(order_id=admin_verified_order['order_id'], administration_process=False,
                                     warehouseAdmin_confirmed=False).all().first()
        order.sent_date = timezone.now()
        order.warehouseAdmin_confirmed = True
        order.save()
        send_verification_sms(order.customer.phone, "کاربر گرامی، سفارش شما از از انبار خارج شد")
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@login_required(login_url='/admin/')
def reject_order(request):
    user = request.user
    if user.groups.filter(name__in=[admins[2], ]).exists():
        admin_verified_order = request.data['order']
        order = Order.objects.filter(order_id=admin_verified_order['order_id'],
                                     sellAdmin_confirmed=False).all().first()
        order.administration_process = True
        order.save()
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_200_OK)


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
