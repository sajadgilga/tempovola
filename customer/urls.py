from django.urls import path

from customer.views import login_, enter_shop, logout_, fetch_data, profile, checkout, enter_checkout, \
    checkout_data

urlpatterns = [
    path('login/', login_),
    path('logout/', logout_),
    path('shop/', enter_shop),
    path('get_shop_data/', fetch_data),
    path('profile/', profile),
    path('checkout/', checkout),
    path('enter_checkout/', enter_checkout),
    path('checkout_data/', checkout_data),
]