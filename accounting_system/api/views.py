from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import (
    OrgCreateSerializer, OrgStorDistSerializer, OrgStorDistCreateSerializer,
    WasteSerializer)
from core.constants import WASTE_NAMES
from core.models import Organization, Waste

User = get_user_model()


@api_view(['GET'])
def get_storages(request):
    """Показывает список всех хранилищ и расстояний до них."""
    try:
        org = request.user.organization
        serializer = OrgStorDistSerializer(org.distances.all(), many=True)
    except Organization.DoesNotExist:
        return Response(
            {'errors': 'Вы не установили организацию.'},
            status.HTTP_400_BAD_REQUEST
        )
    return Response(serializer.data)


@api_view(['POST'])
def create_organization(request):
    """Создаёт организацию."""
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
def add_storage_dist(request):
    """Добавляет расстояние от организации пользователя до хранилища."""
    try:
        org = request.user.organization
        serializer = OrgStorDistCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organization=org)
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
    """Отправляет отходы на переработку в хранилища."""
    try:
        org = request.user.organization
    except Organization.DoesNotExist:
        return Response(
            {'errors': 'Вы не установили организацию.'},
            status.HTTP_400_BAD_REQUEST
        )
    storages = org.distances.all()
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
        for index in range(length):
            waste_name = waste_names[index]
            if org_waste_values.get(waste_name) == 0:
                continue
            limit_name = limits_names[index]
            if waste_stor[limit_name] - waste_stor[waste_name] == 0:
                continue
            waste_stor[waste_name] += org_waste_values[waste_name]
            res = waste_stor[limit_name] - waste_stor[waste_name]
            if res < 0:
                waste_stor[waste_name] -= abs(res)
                org_waste_values[waste_name] = abs(res)
            else:
                org_waste_values[waste_name] = 0
                org.waste.__dict__[waste_name] = 0
                org.waste.save(update_fields=[waste_name])
            filled_storages.append(stor_dist.storage.waste)
        if not any(org_waste_values.values()):
            break
    if not filled_storages:
        return Response({'detail': 'Все хранилища уже заполнены.'})
    Waste.objects.bulk_update(filled_storages, waste_names)
    exccess = [name for name in org_waste_values
               if org_waste_values[name] > 0]
    if exccess:
        return Response({'no_space_for': exccess})
    result = storages.filter(storage__waste__in=filled_storages)
    serializer = OrgStorDistSerializer(result, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PATCH'])
def refil_or_check_org_stock(request):
    """Заполняет запасы отходов организации."""
    try:
        org_waste = request.user.organization.waste
    except Organization.DoesNotExist:
        return Response(
            {'errors': 'Вы не установили организацию.'},
            status.HTTP_400_BAD_REQUEST
        )
    if request.method == 'PATCH':
        org_waste.refill()
    serializer = WasteSerializer(org_waste)
    return Response(serializer.data)
