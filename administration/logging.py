import os
import datetime

from django.utils import timezone
from persiandate import jalali

from TempoVola.settings import ADMIN_LOG_DIR


def success(admin, message):
    write_formatted_message(admin, message, 'INFO/SUCCESS')


def access_deny(admin, message):
    write_formatted_message(admin, message, 'WARNING/ACCESS_DENY')


def info(admin, message):
    write_formatted_message(admin, message, 'INFO')


def error(admin, message):
    write_formatted_message(admin, message, 'ERROR')


def critical(admin, message):
    write_formatted_message(admin, message, 'CRITICAL')


def warning(admin, message):
    write_formatted_message(admin, message, 'WARNING')


def write_formatted_message(admin, message, msg_type):
    now = timezone.now()
    persian_date = jalali.Gregorian(now.strftime('%Y-%m-%d')).persian_string()
    line = '{date} {time} - {type}: {msg} __ {user}\n'.format(date=persian_date, time=now.strftime('%H:%M:%S'),
                                                              type=msg_type,
                                                              msg=message, user=admin)
    path = os.path.join(ADMIN_LOG_DIR, admin.username)
    write_to_file(path, line)


def write_to_file(path, line):
    with open(path, "a+") as file:
        file.write(line)


log_messages = {
    'login_platform_success': 'موفقیت در ورود به سامانه',
    'logout_platform_success': 'موفقیت در خروج از سامانه',
    'fetch_order_data': 'درخواست سفارشات',
    'fetch_order_data_access_deny': 'درخواست سفارشات بدون دسترسی',
    'verify_order_try': 'اقدام به تایید سفارش',
    'verify_order_success': 'موفقیت در تایید سفارش',
    'verify_order_failure': 'عدم تایید سفارش به دلیل ارور پیش آمده',
    'verify_order_access_deny': 'اقدام به تایید سفارش بدون دسترسی',
    'reject_order_try': 'اقدام به رد سفارش',
    'reject_order_success': 'موفقیت در رد سفارش',
    'reject_order_failure': 'عدم رد سفارش به دلیل ارور پیش آمده',
    'reject_order_access_deny': 'اقدام به رد سفارش بدون دسترسی',
    'get_excel_try': 'اقدام به دریافت اکسل گزارشات',
    'get_excel_success': 'موفقیت در دریافت اکسل گزارشات',
    'get_excel_failure': 'عدم دریافت اکسل گزارشات به علت رخداد ارور',
    'search_order_try': 'اقدام به جستجوی سفارشات',
    'search_order_success': 'موفقیت در جستجوی سفارشات',
    'search_order_failure': 'عدم تکمیل جستجو به علت رخداد ارور',
    'search_order_access_deny': 'اقدام به جستجوی سفارشات بدون دسترسی',
    'get_products_for_customer_managing_try': 'اقدام به دریافت محصولات برای مدیریت مشتریان',
    'get_products_for_customer_managing_failure': 'عدم دریافت محصولات برای مدیریت مشتریان به علت رخداد ارور',
    'get_products_for_customer_managing_success': 'موفقیت در دریافت محصولات برای مدیریت مشتریان',
    'signup_customer_try': 'اقدام به ایجاد مشتری جدید',
    'signup_customer_success': 'موفقیت در ایجاد مشتری جدید',
    'signup_customer_failure': 'عدم امکان ایجاد مشتری جدید به علت رخداد ارور',
    'signup_customer_access_deny': 'اقدام به ایجاد مشتری جدید بدون دسترسی',
    'enter_profile_editor_try': 'اقدام به ورود به تغییر پروفایل کاربر',
    'enter_profile_editor_success': 'موفقیت در ورود به تغییر پروفایل کاربر',
    'enter_profile_editor_access_deny': 'اقدام به ورود به تغییر پروفایل کاربر بدون دسترسی',
    'submit_customer_change_try': 'اقدام به تغییر پروفایل کاربر',
    'submit_customer_change_success': 'موفقیت در تغییر پروفایل کاربر',
    'submit_customer_change_failure': 'عدم تغییر پروفایل کاربر به علت رخداد ارور',
    'submit_customer_change_access_deny': 'اقدام به تغییر پروفایل کاربر بدون دسترسی',
    'delete_customer_try': 'اقدام به حذف کاربر',
    'delete_customer_success': 'موفقیت در حذف کاربر',
    'delete_customer_failure': 'عدم حذف کاربر به علت رخداد ارور',
    'delete_customer_access_deny': 'اقدام به حذف کاربر بدون دسترسی',
    'get_melodies': 'دریافت لیست ملودی ها',
    'submit_product_try': 'اقدام به ایجاد محصول',
    'submit_product_success': 'موفقیت در ایجاد محصول',
    'submit_product_failure': 'ایراد در ایجاد محصول',
    'submit_product_access_deny': 'عدم دسترسی به ایجاد محصول',
    'promotion_editor_access_deny': 'عدم دسترسی به ورود به صفحه ایجاد سناریو تخفیف',
    'promotion_editor_access_failure': 'ایراد در ورود ایجاد سناریو تخفیف',
    'get_customer_report_try': 'اقدام به دریافت لیست گزارشات کاربران',
    'get_customer_report_success': 'دریافت لیست گزارشات کاربران',
    'get_customer_report_access_deny': 'عدم دسترسی به لیست گزارشات کاربران',
    'get_customer_report_failure': 'عدم دریافت لیست گزارشات کاربران به علت رخداد ارور',
    'send_customer_report_answer_try': 'اقدام به پاسخ به مشتری',
    'send_customer_report_answer_success': 'پاسخ موفق به مشتری',
    'send_customer_report_answer_access_deny': 'عدم دسترسی به ارسال پاسخ به مشتری',
    'send_customer_report_answer_failure': 'عدم ارسال پاسخ به مشتری به علت رخداد ارور',

    'order_create_try': 'اقدام به ایجاد سفارش',
}
