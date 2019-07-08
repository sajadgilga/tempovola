from django.urls import path

from customer.views.authentication import *
from customer.views.order_making import *
from customer.views.checkout import *

urlpatterns = [
    path('login/', login_),
    path('logout/', logout_),
    path('shop/', enter_shop),
    path('shop/<str:series>/', enter_shop),
    path('get_shop_data/', fetch_data),
    path('profile/', profile),
    path('checkout/', checkout),
    path('enter_checkout/', enter_checkout),
    path('checkout_data/', get_checkout_data),
    path('confirm_checkout/', confirm_checkout),
    path('confirmed_checkout/', enter_confirm_checkout),
    path('fetch_receipt/', get_receipt),
    path('music/', get_music),
    path('send_report/', send_report),
    path('get_orders_report/', get_orders_report)
]
