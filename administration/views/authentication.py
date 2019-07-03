import json

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
        if not user.groups.filter(name__in=['admin']).exists():
            return Response({'msg': 'سطح دسترسی لازم را ندارید'}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({'msg': 'login successful'}, status=status.HTTP_200_OK)
    except:
        return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def logout_(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)

