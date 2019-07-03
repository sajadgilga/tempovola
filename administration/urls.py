from django.urls import path

from administration.views.authentication import *
from administration.views.customer_managing import *
from administration.views.order_managing import *

urlpatterns = [
    path('', enter_admin_login),
    path('login/', login_),
    path('logout/', logout_),
    path('dashboard/', enter_dashboard),
    path('profile_maker/', profile_maker),
    path('product_maker/', product_maker),
    path('order_excl/', get_order_excel),
    path('order_list/', get_order_list),
    path('product_series/', get_products),
    path('submit_customer/', signup_customer),
    path('fetch_orders/', get_orders),
]
