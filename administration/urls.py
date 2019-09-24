from django.urls import path

from administration.views.authentication import *
from administration.views.customer_managing import *
from administration.views.order_managing import *
from administration.views.product_managing import *

urlpatterns = [
    path('', enter_admin_login),
    path('login/', login_),
    path('logout/', logout_),
    path('dashboard/', enter_dashboard),
    path('get_dashboard_elements/', get_dashboard_elements),
    path('profile_maker/', profile_maker),
    path('profile_editor/', profile_editor),
    path('product_maker/', enter_product_maker),
    path('order_excl/', get_order_excel),
    path('order_list/', get_order_list),
    path('product_series/', get_products),
    path('submit_customer/', signup_customer),
    path('fetch_orders/', get_orders),
    path('verify_order/', verify_order),
    path('reject_order/', reject_order),
    path('melodies/', get_melodies),
    path('submit_product/', submit_product),
    path('submit_customer_change/', submit_customer_change),
    path('search_customer/', search_customer),
    path('delete_customer/', delete_customer),
    path('search_orders_page/', search_orders_page),
    path('search_orders/', search_orders),
]
