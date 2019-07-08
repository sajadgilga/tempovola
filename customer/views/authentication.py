import json

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from persiandate import jalali
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from customer.models import CustomerProfile, Report, Order
from customer.serializers import CustomerSerializer, OrderSerializer


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
def send_report(request):
    try:
        user = request.user
        report = Report()
        report.description = request.data['report']
        report.owner = user
        report.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_required(login_url='/admin/')
def get_orders_report(request):
    try:
        user = request.user
        customer = CustomerProfile.objects.filter(user=user).all().first()
        orders = Order.objects.filter(customer=customer) \
            .all().order_by('-created_date')
        orders = OrderSerializer(orders, many=True).data
        orders = json.loads(JSONRenderer().render(orders))
        for order in orders:
            order['created_date'] = jalali.Gregorian(order['created_date'].split('T')[0]).persian_string()
        return Response({'orders': orders})
    except:
        return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

