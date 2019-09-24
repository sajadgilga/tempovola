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

from administration import logging
from administration.logging import log_messages
from customer.models import Order, ShopItem, SchemaSeries, CustomerProfile, Series, Melody

admins = ['admin', 'orderAdmin', 'sellAdmin', 'warehouseAdmin', 'financeAdmin', 'customerAdmin', 'productAdmin',
          'monitorAdmin', 'administrator']
admin_rights = {
    admins[0]: {},
    admins[1]: {
        'گزارشات': 1,
        'ایجاد سفارش': 4
    },
    admins[2]: {
        'گزارشات': 1
    },
    admins[3]: {
        'گزارشات': 1
    },
    admins[4]: {
        'گزارشات': 1
    },
    admins[5]: {
        'ایجاد کاربر': 5,
        'گزارشات کاربران': 6,
        'تغییر کاربر': 9,
        'جستجو': 2
    },
    admins[6]: {
        'ایجاد محصول': 7
    },
    admins[7]: {
        'مانیتور ادمین': 8,
        'ایجاد ادمین': 10
    },

    admins[8]: {
        'گزارشات': 1,
        'جستجو': 2,
        'دریافت فایل اکسل': 3
    },
}


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
    customer.state = form['state']
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
        series.price = schema_series.price
        series.product_code = schema_series.product_code
        series.description = schema_series.description
        series.picture = schema_series.picture
        series.save()
        for mel_name in form['melodies'][product]:
            mel_schema = schema_series.melodies.get(name=mel_name)
            # melody = Melody()
            # melody.name = mel_name
            # melody.melody_code = mel_schema.melody_code
            # melody.price = mel_schema.price
            # melody.save()
            series.melodies.add(mel_schema)
        series.save()
        customer.available_series.add(series)
    customer.save()


# main function for signing up new users
def create_new_user(form):
    user = User.objects.create_user(username=form[form['username_type'][0]],
                                    email=form['email'], password=form['password'])
    customer = create_new_customer(form, user)
    fill_available_series(form, customer)


def getAdminDashboard(user):
    new_orders = 0
    choice_list = {}
    if user.groups.filter(name__in=[admins[1], ]).exists():
        new_orders = len(Order.objects.filter(orderAdmin_confirmed=False, is_checked_out=True,
                                              administration_process=False).all())
    elif user.groups.filter(name__in=[admins[2], ]).exists():
        new_orders = len(Order.objects.filter(orderAdmin_confirmed=True, sellAdmin_confirmed=False,
                                              administration_process=False).all())
    elif user.groups.filter(name__in=[admins[3], ]).exists():
        new_orders = len(Order.objects.filter(sellAdmin_confirmed=True, warehouseAdmin_confirmed=False,
                                              administration_process=False).all())
    elif user.groups.filter(name__in=[admins[4], ]).exists():
        new_orders = len(Order.objects.filter(warehouseAdmin_confirmed=True, financeAdmin_confirmed=False,
                                              administration_process=False).all())
    elif user.groups.filter(name__in=[admins[8], ]).exists():
        new_orders = len(Order.objects.filter(administration_process=True).all())
    for admin in user.groups.values_list('name', flat=True):
        for right, value in admin_rights[admin].items():
            choice_list[right] = value
    return {'new_orders': new_orders, "choice_list": choice_list}


@api_view(['GET'])
@login_required(login_url='/admin/')
def enter_dashboard(request):
    try:
        user = request.user
        if not check_access(user):
            return Response({'msg': 'سطح دسترسی لازم را ندارید'}, status=status.HTTP_401_UNAUTHORIZED)
        return render(request, 'admin/admin_dashboard.html')
    except:
        return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@login_required(login_url='/admin/')
def get_dashboard_elements(request):
    # try:
    user = request.user
    if not check_access(user):
        return Response({'msg': 'سطح دسترسی لازم را ندارید'}, status=status.HTTP_401_UNAUTHORIZED)
    new_orders = getAdminDashboard(user)
    access = user.groups.all()
    return Response(
        {
            'newOrders': new_orders['new_orders'],
            'rights': new_orders['choice_list'],
            'name': user.username
        })
    # except:
    #     return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    user = request.user
    logging.info(user, log_messages['get_products_for_customer_managing_try'])
    try:
        products = SchemaSeries.objects.all().values_list('name', 'melodies__name')
        logging.success(user, log_messages['get_products_for_customer_managing_success'])
        return Response({'products': products}, status=status.HTTP_200_OK)
    except:
        logging.error(user, log_messages['get_products_for_customer_managing_failure'])
        return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@login_required(login_url='/admin/')
def signup_customer(request):
    user = request.user
    logging.info(user, log_messages['signup_customer_try'])
    try:
        if not user.groups.filter(name__in=[admins[5],]).exists():
            logging.access_deny(user, log_messages['signup_customer_access_deny'])
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        form = request.data['form']
        if CustomerProfile.objects.filter(email=form['email']).exists():
            return Response({'msg': 'ایمیل مورد نظر قبلا در سامانه ثبت شده است'},
                            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        if 'phone' in form['username_type']:
            if CustomerProfile.objects.filter(phone=form['phone']).exists():
                return Response({'msg': 'شماره تماس مورد نظر قبلا در سامانه ثبت شده است'},
                                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        create_new_user(form)
        if form['phone'] is not None and form['phone'] != '':
            api = KavenegarAPI('6652373751486A6D5A34584B476A466F346E616F7A313768553441726330554E')
            params = {
                'sender': '1000596446',
                'receptor': form['phone'],
                'message': "کاربر گرامی، حساب کاربری شما در سامانه tempovola با موفقیت ثبت گردید.".encode('utf-8')
            }
            # try:
            response = api.sms_send(params)
            # except:
                # print("شماره کاربر مشکل دارد")
                # return Response({"msg": "شماره تلفن کاربر ایراد دارد: " + form['phone']},
                #                 status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        logging.success(user, log_messages['signup_customer_success'])
        return Response(status=status.HTTP_200_OK)
    except:
        logging.error(user, log_messages['signup_customer_failure'])
        return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@login_required(login_url='/admin/')
def profile_editor(request):
    user = request.user
    logging.info(user, log_messages['enter_profile_editor_try'])
    if request.user.groups.filter(name__in=[admins[5], ]).exists():
        logging.success(user, log_messages['enter_profile_editor_success'])
        return render(request, 'admin/profile_editor.html', {'name': request.user.username})
    logging.access_deny(user, log_messages['enter_profile_editor_access_deny'])
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@login_required(login_url='/admin/')
def submit_customer_change(request):
    user = request.user
    logging.info(user, log_messages['submit_customer_change_try'])
    try:
        if not user.groups.filter(name__in=[admins[5], ]).exists():
            logging.access_deny(user, log_messages['submit_customer_change_access_deny'])
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        form = request.data['form']
        customer = CustomerProfile.objects.filter(email=form['email']).all().first()
        if not customer:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        customer.company_name = form['company_name']
        customer.phone = form['phone']
        customer.city = form['city']
        customer.address = form['address']
        customer.state = form['state']
        Series.objects.filter(customerprofile__email=customer.email).all().delete()
        customer.save()
        fill_available_series(form, customer)
        logging.success(user, log_messages['submit_customer_change_success'])
        return Response(status=status.HTTP_200_OK)
    except:
        logging.error(user, log_messages['submit_customer_change_failure'])
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@login_required(login_url='/admin/')
def search_customer(request):
    if not CustomerProfile.objects.filter(email=request.data['email']).exists():
        return Response({'msg': 'کاربر یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
    customer = CustomerProfile.objects.filter(email=request.data['email']).all().first()
    available_series = []
    melodies = {}
    for series in customer.available_series.all():
        melodies[series.name] = series.melodies.all().values_list('name', flat=True)
        available_series.append(series.name)
    return Response({'customer': {
        'company_name': customer.company_name,
        'email': customer.email,
        'phone': customer.phone.base_number,
        'city': customer.city,
        'state': customer.state,
        'address': customer.address,
        'available_series': available_series,
        'melodies': melodies
    }}, status=status.HTTP_200_OK)


@api_view(['POST'])
@login_required(login_url='/admin/')
def delete_customer(request):
    user = request.user
    logging.info(user, log_messages['delete_customer_try'])
    try:
        if not user.groups.filter(name__in=[admins[5], ]).exists():
            logging.access_deny(user, log_messages['delete_customer_access_deny'])
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not CustomerProfile.objects.filter(email=request.data['email']).exists():
            return Response({'msg': 'کاربر یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            CustomerProfile.objects.filter(email=request.data['email']).all().first().delete()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            User.objects.filter(username=request.data['email']).all().first().delete()
        logging.success(user, log_messages['delete_customer_success'])
        return Response(status=status.HTTP_200_OK)
    except:
        logging.error(user, log_messages['delete_customer_failure'])
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
