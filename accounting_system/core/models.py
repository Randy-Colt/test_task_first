from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CheckConstraint, F, UniqueConstraint, Q

User = get_user_model()


class Waste(models.Model):
    biowaste = models.PositiveSmallIntegerField(
        verbose_name='Биоотходы', default=0, blank=True
    )
    glass = models.PositiveSmallIntegerField(
        verbose_name='Стекло', default=0, blank=True
    )
    plastic = models.PositiveSmallIntegerField(
        verbose_name='Пластик', default=0, blank=True
    )
    biowaste_max = models.PositiveSmallIntegerField(
        verbose_name='Предел биоотходов', default=0, blank=True
    )
    glass_max = models.PositiveSmallIntegerField(
        verbose_name='Предел стекла', default=0, blank=True
    )
    plastic_max = models.PositiveSmallIntegerField(
        verbose_name='Предел пластика', default=0, blank=True
    )

    class Meta:
        verbose_name = 'Отходы'
        verbose_name_plural = 'Отходы'
        constraints = (
            CheckConstraint(
                check=Q(biowaste__lte=F('biowaste_max')),
                name='check_biowaste'
            ),
            CheckConstraint(
                check=Q(glass__lte=F('glass_max')),
                name='check_glass'
            ),
            CheckConstraint(
                check=Q(plastic__lte=F('plastic_max')),
                name='check_plastic'
            )
        )


class Storage(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50)
    waste = models.OneToOneField(Waste, on_delete=models.CASCADE)
    nearby_storage = models.ManyToManyField(
        'self',
        through='StorageDistance',
        symmetrical=True,
        through_fields=('storage', 'neighbour_storage')
    )


class Organization(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50)
    storage = models.ManyToManyField(
        Storage,
        through='OrganizationStorageDist'
    )
    waste = models.OneToOneField(
        Waste,
        on_delete=models.CASCADE,
        related_name='waste',
        verbose_name='Отходы'
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='organization'
    )


class StorageDistance(models.Model):
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        related_name='neighbour',
        verbose_name='Хранилище'
    )
    neighbour_storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        verbose_name='Соседнее хранилище'
    )
    distance = models.PositiveIntegerField(verbose_name='Расстояние')

    class Meta:
        ordering = 'distance',
        constraints = (
            CheckConstraint(
                check=~Q(storage=F('neighbour_storage')),
                name='check_create_self_as_neighbour'
            ),
            UniqueConstraint(
                fields=('storage', 'neighbour_storage'),
                name='check_storage_neighbour_unique_constraint'
            )
        )


class OrganizationStorageDist(models.Model):
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        related_name='organizations',
        verbose_name='Хранилище'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='storages',
        verbose_name='Организация'
    )
    distance = models.PositiveIntegerField(verbose_name='Расстояние')

    class Meta:
        ordering = 'distance',
        constraints = [
            UniqueConstraint(
                fields=('organization', 'storage'),
                name='check_org_storage_unique_constraint'
            )
        ]
