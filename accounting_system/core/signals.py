from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import OrganizationStorageDist, StorageDistance

@receiver(post_save, sender=StorageDistance)
def create_path_to_org(sender, instance, created, **kwargs):
    """
    Создаёт длину маршрута от нового хранилища до организации.

    Для активации сигнала необходимо создать дистанцию между хранилищами
    напрямую, как показано в примере.
    Пример: StorageDistance.objects.create(storage=<new_storage>,
    neighbour_storage=<old_storage>, distance=<some_distance>)
    """
    if created:
        neighbour_storage = instance.neighbour_storage
        new_storage = instance.storage
        if not OrganizationStorageDist.objects.filter(
                storage=new_storage).exists():
            inst_dist = instance.distance
            orgs_dist = OrganizationStorageDist.objects.filter(
                storage=neighbour_storage)
            OrganizationStorageDist.objects.bulk_create(
                OrganizationStorageDist(
                    organization=item.organization,
                    storage=new_storage,
                    distance=item.distance + inst_dist
                ) for item in orgs_dist
            )
