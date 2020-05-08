import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from TempoVola.settings import admins
from administration import logging
from administration.logging import log_messages


@api_view(['GET'])
def enter_admin_login(request):
    return render(request, 'admin/adminlogin.html')


@api_view(['POST'])
def login_(request):
    try:
        body = request.body
        user_data = json.loads(body)
        user = authenticate(request, username=user_data['username'], password=user_data['password'])
        if user is None:
            return Response({'msg': 'اطلاعات وارد شده غلط می‌باشد. دوباره تلاش کنید'},
                            status=status.HTTP_401_UNAUTHORIZED)
        if not user.groups.filter(name__in=admins).exists():
            return Response({'msg': 'سطح دسترسی لازم را ندارید'}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        logging.success(user, log_messages['login_platform_success'])
        return Response({'msg': 'login successful'}, status=status.HTTP_200_OK)
    except:
        return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def logout_(request):
    user = request.user
    logout(request)
    logging.success(user, log_messages['logout_platform_success'])
    return Response(status=status.HTTP_200_OK)


# TODO: add admin maker page
@api_view(['GET'])
@login_required(login_url='/admin/')
def enter_admin_maker(request):
    pass
