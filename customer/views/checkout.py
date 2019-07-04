import json

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import  HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from kavenegar import KavenegarAPI
from persiandate import jalali
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from weasyprint import HTML

from customer.models import CustomerProfile, Order, ShopItem
from customer.serializers import OrderSerializer, ItemSerializer


def get_persian_date(date):
    date = jalali.Gregorian(date).persian_string().split('-')
    date = date[2] + '-' + date[1] + '-' + date[0]
    return date


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
    # try:
    user = request.user
    customer = CustomerProfile.objects.get(user=user)
    order = Order.objects.filter(customer=customer).all().last()
    order.is_checked_out = True
    order.save()

    if customer.phone is not None:
        api = KavenegarAPI('6652373751486A6D5A34584B476A466F346E616F7A313768553441726330554E')
        params = {
            'sender': '1000596446',
            'receptor': customer.phone.raw_phone,
            'message': ("کاربر گرامی، سفارش شما با کد " + order.order_id + " با موفقیت ثبت گردید").encode('utf-8')
        }
        try:
            response = api.sms_send(params)
        except:
            print("شماره کاربر وجود ندارد", customer.phone.raw_phone)
    return Response(status=status.HTTP_200_OK)
    # except:
    #     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@login_required(login_url='/')
def enter_confirm_checkout(request):
    return render(request, 'customer/confirm_receipt.html')


@api_view(['GET'])
@login_required(login_url='/')
def get_receipt(request):
    try:
        user = request.user
        order = Order.objects.filter(customer=CustomerProfile.objects.get(user=user)).all().last()
        items = ShopItem.objects.filter(order=order)
        items = ItemSerializer(items, many=True)
        items = JSONRenderer().render(items.data)
        items = json.loads(items)
        html_string = render_to_string('customer/receipt.html',
                                       {
                                           'items': items,
                                           'ordercode': order.order_id,
                                           'date': get_persian_date(order.created_date.strftime('%Y-%m-%d')),
                                           'name': order.customer.company_name,
                                           'discount': 0,
                                           'total_price': order.cost,
                                       })

        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/mypdf.pdf')

        fs = FileSystemStorage('/tmp')
        with fs.open('mypdf.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
            return response
        return response
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

