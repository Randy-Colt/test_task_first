from rest_framework import serializers

from api.add_storages import set_all_storages
from core.models import (
    Organization, OrganizationStorageDist, Storage, Waste)


class WasteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Waste
        exclude = 'id',

    def validate(self, attrs):
        limits = (attrs.get('biowaste_max'), attrs.get('glass_max'), attrs.get('plastic_max'))
        any_max = any(limits)
        if not any_max:
            raise serializers.ValidationError(
                'Должен быть установлен хотя бы один предел отходов.'
            )
        for limit in limits:
            if limit < 0:
                raise serializers.ValidationError(
                    'Предел не может быть отрицательным.'
                )
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        result = {}
        for key, value in representation.items():
            if value is not None:
                result[key] = value
        return result


class OrgCreateSerializer(serializers.ModelSerializer):
    waste = WasteSerializer()

    class Meta:
        model = Organization
        fields = ('name', 'waste')

    def validate_waste(self, value):
        if not value:
            raise serializers.ValidationError('Это поле не может быть пустым.')
        return value

    def create(self, validated_data):
        waste_dct = validated_data.pop('waste')
        waste = Waste.objects.create(**waste_dct)
        return Organization.objects.create(waste=waste, **validated_data)


class OrgStorageDistSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='storage.name')
    waste = WasteSerializer(source='storage.waste')

    class Meta:
        model = OrganizationStorageDist
        fields = ('name', 'waste', 'distance')


class StorageListSerializer(serializers.ModelSerializer):
    storages = OrgStorageDistSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = 'storages',


class OrgStorDistCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationStorageDist
        fields = ('storage', 'distance')

    def validate_distance(self, value):
        if not value:
            raise serializers.ValidationError('Это поле не может быть пустым.')
        if value <= 0:
            raise serializers.ValidationError(
                'Расстояние не может быть отрицательным или равняться нулю.'
            )
        return value

    def validate_storage(self, value):
        if not value:
            raise serializers.ValidationError('Это поле не может быть пустым.')
        return value

    def create(self, validated_data):
        storage = validated_data.pop('storage')
        dist = validated_data.get('distance')
        new_org = validated_data.get('organization')
        if not OrganizationStorageDist.objects.filter(organization=new_org)\
            .exists():
            set_all_storages(new_org, storage, dist)
        org_stor_dist = OrganizationStorageDist.objects.create(
            storage=storage, **validated_data)
        return org_stor_dist
