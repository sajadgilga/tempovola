
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from administration.views.customer_managing import admins
from customer.models import Melody, Series, SchemaSeries


@api_view(['GET'])
@login_required(login_url='/admin/')
def get_melodies(request):
    melodies = Melody.objects.values_list('name', flat=True)
    melodies = list(set(melodies))
    return Response({'melodies': melodies})


@api_view(['GET'])
@login_required(login_url='/admin/')
def enter_product_maker(request):
    try:
        user = request.user
        return render(request, 'admin/product_maker.html', {'name': user.username})
    except:
        return Response({'msg': 'مشکلی در سرور به وجود آمده'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@login_required(login_url='/admin/')
def submit_product(request):
    try:
        user = request.user
        if not user.groups.filter(name__in=[admins[6], ]).exists():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        product = request.data['form']
        product_name = product['name']
        product_code = product['code']
        product_price = product['price']
        product_desc = product['desc']
        if product['isMelody']:
            if Melody.objects.filter(name=product_name).exists():
                new_melody = Melody.objects.filter(name=product_name).all().first()
            else:
                new_melody = Melody()
            new_melody.name = product_name
            new_melody.melody_code = product_code
            # new_melody.music
            new_melody.save()
        else:
            if Melody.objects.filter(name=product_name).exists():
                new_series = SchemaSeries.objects.filter(name=product_name).all().first()
            else:
                new_series = SchemaSeries()
            new_series.name = product_name
            new_series.product_code = product_code
            new_series.description = product_desc
            new_series.price = product_price
            for i in range(len(product_name)):
                try:
                    melody = Melody.objects.get(name=product_name[i])
                    new_series.melodies.add(melody)
                except:
                    return Response({'msg': product_name[i] + ' is not in database'}, status=status.HTTP_400_BAD_REQUEST)
            # new_series.picture
            new_series.save()
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
