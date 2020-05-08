from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import permissions, authentication, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from TempoVola.settings import admins
from administration import logging
from administration.logging import log_messages


@api_view(['GET'])
@login_required(login_url='/admin/')
def monitor_page(request):
    user = request.user
    if not user.groups.filter(name__in=[admins[5], ]).exists():
        logging.access_deny(user, log_messages[''])
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    admin_list = User.objects.filter(groups__name__in=admins).values('username')
    return render(request, 'admin/admin_monitor.html', context={
        'admin_list': admin_list
    })


@api_view(['POST'])
@login_required(login_url='/admin/')
def get_admin_logs(request):
    pass
