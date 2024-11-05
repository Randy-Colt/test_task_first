from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CheckConstraint, F, UniqueConstraint, Q

User = get_user_model()


class Waste(models.Model):
    """
    Модель хранения отходов.

    При создании организации или хранилища должен быть указан экземпляр
    этой модели.
    """

    biowaste = models.PositiveSmallIntegerField(
        default=0, blank=True, verbose_name='Биоотходы'
    )
    glass = models.PositiveSmallIntegerField(
        default=0, blank=True, verbose_name='Стекло'
    )
    plastic = models.PositiveSmallIntegerField(
        default=0, blank=True, verbose_name='Пластик'
    )
    biowaste_max = models.PositiveSmallIntegerField(
        default=0, blank=True, verbose_name='Предел биоотходов'
    )
    glass_max = models.PositiveSmallIntegerField(
        default=0, blank=True, verbose_name='Предел стекла'
    )
    plastic_max = models.PositiveSmallIntegerField(
        default=0, blank=True, verbose_name='Предел пластика'
    )

    class Meta:
        verbose_name = 'Отходы'
        verbose_name_plural = 'Отходы'
        ordering = 'id',
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

    def refill(self) -> None:
        """Заполнить хранилище мусора до максимума."""
        self.biowaste = self.biowaste_max
        self.glass = self.glass_max
        self.plastic = self.plastic_max
        return self.save(update_fields=('biowaste', 'glass', 'plastic'))

    def __str__(self):
        return f'{self.pk}'


class Storage(models.Model):
    """
    Модель хранилища.

    Новое хранилище может создавать только администратор.
    """

    name = models.CharField(verbose_name='Название', max_length=50)
    waste = models.OneToOneField(
        Waste,
        on_delete=models.CASCADE,
        verbose_name='id модели отходов',
    )
    nearby_storages = models.ManyToManyField(
        'self',
        through='StorageDistance',
        symmetrical=True,
        through_fields=('storage', 'neighbour_storage')
    )

    class Meta:
        verbose_name = 'Хранилище'
        verbose_name_plural = 'Хранилища'
        ordering = 'name',

    def __str__(self):
        return f'{self.name}'


class Organization(models.Model):
    """
    Модель организации, может быть связана только с одним пользователем.

    Для использования API сервиса к пользователю должна быть привязана
    организация.
    """

    name = models.CharField(verbose_name='Название', max_length=50)
    storages = models.ManyToManyField(
        Storage,
        through='OrganizationStorageDist'
    )
    waste = models.OneToOneField(
        Waste,
        on_delete=models.CASCADE,
        related_name='waste',
        verbose_name='id модели отходов'
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='organization',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = 'name',

    def __str__(self):
        return f'{self.name}'


class StorageDistance(models.Model):
    """
    Модель для хранения расстояний между хранилищами.

    После создания связи нового хранилища с уже существующем активируется
    сигнал core.signals.create_path_to_org(). Создаёт только администратор.
    """

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
        verbose_name = 'Хранилище-сосед'
        verbose_name_plural = 'Хранилища-соседи'
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
    """
    Модель для хранения расстояний между организациями и хранилищами.

    Пользователь с привязанной организацией может самостоятельно указать
    расстояние от организации до хранилища.
    """

    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        related_name='organizations',
        verbose_name='Хранилище'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='distances',
        verbose_name='Организация'
    )
    distance = models.PositiveIntegerField(verbose_name='Расстояние')

    class Meta:
        verbose_name = 'Организация и хранилище'
        verbose_name_plural = 'Организации и хранилища'
        ordering = 'distance',
        constraints = [
            UniqueConstraint(
                fields=('organization', 'storage'),
                name='check_org_storage_unique_constraint'
            )
        ]
