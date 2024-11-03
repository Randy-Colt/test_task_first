from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import (
    OrgStorDistCreateSerializer, OrgCreateSerializer, OrgStorageDistSerializer)
from core.constants import WASTE_NAMES
from core.models import Organization, Waste

User = get_user_model()

@api_view(['GET'])
def get_storages(request):
    try:
        org = request.user.organization
        serializer = OrgStorageDistSerializer(org.storages.all(), many=True)
    except Organization.DoesNotExist:
        return Response(
            {'errors': 'Вы не установили организацию.'},
            status.HTTP_400_BAD_REQUEST
        )
    return Response(serializer.data)

@api_view(['POST'])
def create_organization(request):
    try:
        serializer = OrgCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
    except IntegrityError:
        return Response(
            {'errors': 'Вы уже установили организацию.'},
            status.HTTP_400_BAD_REQUEST
        )
    return Response(serializer.data, status.HTTP_201_CREATED)

@api_view(['POST'])
def add_storage(request):
    try:
        new_org = request.user.organization
        serializer = OrgStorDistCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organization=new_org)
    except Organization.DoesNotExist:
        return Response(
            {'errors': 'Вы не установили организацию.'},
            status.HTTP_400_BAD_REQUEST
        )
    except IntegrityError:
        return Response(
            {'errors': 'Вы уже добавили это хранилище.'},
            status.HTTP_400_BAD_REQUEST
        )
    return Response(serializer.data, status.HTTP_201_CREATED)

@api_view(['POST'])
def send_waste(request):
    try:
        org = request.user.organization
    except Organization.DoesNotExist:
        return Response(
            {'errors': 'Вы не установили организацию.'},
            status.HTTP_400_BAD_REQUEST
        )
    storages = org.storages.all()
    org_waste_values = {key: org.waste.__dict__[key] for key in WASTE_NAMES
                        if org.waste.__dict__[key] > 0}
    length = len(org_waste_values)
    if length == 0:
        return Response(
            {'errors': 'Ваш запас отходов уже пуст.'},
            status.HTTP_400_BAD_REQUEST
        )
    waste_names = [name for name in WASTE_NAMES if name in org_waste_values]
    limits_names = [name + '_max' for name in WASTE_NAMES
                    if name in org_waste_values]
    filled_storages = []
    for stor_dist in storages:
        waste_stor = stor_dist.storage.waste.__dict__
        deleteing_list = []
        for index in range(length):
            waste_name = waste_names[index]
            limit_name = limits_names[index]
            if waste_stor[limit_name] - waste_stor[waste_name] == 0:
                continue
            waste_stor[waste_name] += org_waste_values[waste_name]
            res = waste_stor[limit_name] - waste_stor[waste_name]
            if res < 0:
                waste_stor[waste_name] -= abs(res)
                org_waste_values[waste_name] = abs(res)
            else:
                del org_waste_values[waste_name]
                deleteing_list.append(index)
                org.waste.__dict__[waste_name] = 0
                org.waste.save(update_fields=[waste_name])
            filled_storages.append(stor_dist.storage.waste)
        if deleteing_list:
            for name_index in deleteing_list:
                del waste_names[name_index]
                del limits_names[name_index]
                deleteing_list.remove(name_index)
        length = len(org_waste_values)
        if length == 0:
            break
    if not filled_storages:
        return Response({'detail': 'Все хранилища уже заполнены.'})
    Waste.objects.bulk_update(filled_storages, waste_names)
    result = storages.filter(storage__waste__in=filled_storages)
    serializer = OrgStorageDistSerializer(result, many=True)
    return Response(serializer.data)
