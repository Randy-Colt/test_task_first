from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import (
    OrgStorDistCreateSerializer, OrgCreateSerializer, StorageListSerializer)
from core.models import Organization

User = get_user_model()

@api_view(['GET'])
def get_storages(request):
    try:
        serializer = StorageListSerializer(request.user.organization)
        return Response(serializer.data)
    except Organization.DoesNotExist:
        return Response(
            {'errors': 'Вы не установили организацию.'},
            status.HTTP_400_BAD_REQUEST
        )

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
    return Response(serializer.data, status.HTTP_201_CREATED)
