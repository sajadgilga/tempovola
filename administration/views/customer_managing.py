import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from kavenegar import KavenegarAPI
from persiandate import jalali
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from customer.models import Order, ShopItem, SchemaSeries, CustomerProfile, Series, Melody

admins = ['admin', 'orderAdmin', 'sellAdmin', 'warehouseAdmin']


# check if logged in admin has permission to alter panel
def check_access(user):
    if user.groups.filter(name__in=admins):
        return True
    else:
        return False


# generates id according to last customer for new customer being signed up
def get_new_customer_id():
    last_customer_made = CustomerProfile.objects.all().last()
    id_num = '00001'
    if last_customer_made and last_customer_made.customer_id:
        id_num = str(int(last_customer_made.customer_id.split('C')[1]) + 1)
        if len(id_num) < 6:
            id_num = '0' * (6 - len(id_num)) + id_num
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    currentDate = jalali.Gregorian(date).persian_string().split('-')[0]
    id = str(currentDate) + 'C' + id_num
    return id


# creates new customer in database when signed up
def create_new_customer(form, user):
    customer = CustomerProfile()
    customer.user = user
    customer.email = form['email']
    customer.phone = form['phone']
    customer.company_name = form['company_name']
    customer.city = form['city']
    customer.address = form['address']
    customer.customer_id = get_new_customer_id()
    customer.save()
    return customer


## creates available series products for new customer,
# it also limits customers possible musics for every specific series, creates new record of melodies for every customer
# it could be beneficial if each customer did not have different melody record for himself
def fill_available_series(form, customer):
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


# main function for signing up new users
def create_new_user(form):
    user = User.objects.create_user(username=form[form['username_type'][0]],
                                    email=form['email'], password=form['password'])
    customer = create_new_customer(form, user)
    fill_available_series(form, customer)


@api_view(['GET'])
@login_required(login_url='/admin/')
def enter_dashboard(request):
    try:
        user = request.user
        if not check_access(user):
            return Response({'msg': 'سطح دسترسی لازم را ندارید'}, status=status.HTTP_401_UNAUTHORIZED)
        new_orders = 0
        if user.groups.filter(name__in=[admins[1], ]).exists():
            new_orders = len(Order.objects.filter(orderAdmin_confirmed=False, is_checked_out=True,
                                                  administration_process=False).all())
        elif user.groups.filter(name__in=[admins[2], ]).exists():
            new_orders = len(Order.objects.filter(orderAdmin_confirmed=True, sellAdmin_confirmed=False,
                                                  administration_process=False).all())
        elif user.groups.filter(name__in=[admins[3], ]).exists():
            new_orders = len(Order.objects.filter(sellAdmin_confirmed=True, warehouseAdmin_confirmed=False,
                                                  administration_process=False).all())
        access = user.groups.all()
        return render(request, 'admin/admin_dashboard.html',
                      {
                          'newOrders': new_orders,
                          'name': user.username,
                          'access': access
                      })
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
                        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    if 'phone' in form['username_type']:
        if CustomerProfile.objects.filter(phone=form['phone']).exists():
            return Response({'msg': 'شماره تماس مورد نظر قبلا در سامانه ثبت شده است'},
                            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    create_new_user(form)
    if form['phone'] is not None:
        api = KavenegarAPI('6652373751486A6D5A34584B476A466F346E616F7A313768553441726330554E')
        params = {
            'sender': '1000596446',
            'receptor': form['phone'],
            'message': "کاربر گرامی، حساب کاربری شما در سامانه tempovola با موفقیت ثبت گردید.".encode('utf-8')
        }
        try:
            response = api.sms_send(params)
        except:
            print("شماره کاربر مشکل دارد")
            return Response({"msg": "شماره تلفن کاربر ایراد دارد: " + form['phone']},
                            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
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
