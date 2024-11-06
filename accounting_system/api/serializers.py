from rest_framework import serializers

from core.constants import LIMITS_NAMES, WASTE_NAMES
from core.models import (
    Organization, OrganizationStorageDist, Waste)


class WasteSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью отходов."""

    free_space = serializers.SerializerMethodField()

    class Meta:
        model = Waste
        exclude = 'id',

    def validate(self, attrs):
        limits = []
        for name in LIMITS_NAMES:
            limits.append(attrs.get(name))
        if not any(limits):
            raise serializers.ValidationError(
                'Должен быть установлен хотя бы один предел отходов.'
            )
        for limit in limits:
            if limit < 0:
                raise serializers.ValidationError(
                    'Предел не может быть отрицательным.'
                )
        return attrs

    def get_free_space(self, obj):
        obj_dict = obj.__dict__
        result = {}
        names_len = len(WASTE_NAMES)
        for index in range(names_len):
            waste_name = WASTE_NAMES[index]
            limit_name = LIMITS_NAMES[index]
            result[waste_name] = obj_dict.get(limit_name, 0) - obj_dict.get(waste_name, 0)
        return result


class OrgCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания организации."""

    waste = WasteSerializer()

    class Meta:
        model = Organization
        fields = ('name', 'waste')

    def validate_waste(self, value):
        if not value:
            raise serializers.ValidationError('Это поле не может быть пустым.')
        return value

    def create(self, validated_data):
        waste_dict = validated_data.pop('waste')
        waste = Waste.objects.create(**waste_dict)
        return Organization.objects.create(waste=waste, **validated_data)


class OrgStorDistSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода хранилищ и их расстояний до организации."""

    name = serializers.CharField(source='storage.name')
    waste = WasteSerializer(source='storage.waste')

    class Meta:
        model = OrganizationStorageDist
        fields = ('name', 'waste', 'distance')


class OrgStorDistCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для записи расстоянии между организацией и хранилищем."""

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
