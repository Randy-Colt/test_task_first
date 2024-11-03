from django.db import transaction

from core.models import OrganizationStorageDist, StorageDistance


def set_dist_neighbour_storage(storage):
    neighbours = StorageDistance.objects.filter(storage=storage)
    as_neighbors = StorageDistance.objects.filter(neighbour_storage=storage)



def set_all_storages(new_org, storage, dist) -> None:
    related_org = OrganizationStorageDist.objects.filter(
            storage=storage).first()
    related_org_dist = related_org.distance
    related_org = related_org.organization
    neighbour_storages = []
    if hasattr(storage, 'neighbour_storage'):
        neighbour_storages = set_dist_neighbour_storage(storage)
    storages = OrganizationStorageDist.objects.filter(
        organization=related_org)\
            .exclude(storage=storage,storage__in=neighbour_storages)
    with transaction.atomic():
        OrganizationStorageDist.objects.bulk_create(
            OrganizationStorageDist(
                organization=new_org,
                storage=obj.storage,
                distance=dist + related_org_dist + obj.distance
            ) for obj in storages
        )
