from django.db import transaction

from core.models import OrganizationStorageDist


def set_all_storages(new_org, org_stor, dist) -> None:
    related_org = OrganizationStorageDist.objects.filter(
            storage=org_stor).first()
    related_org_dist = related_org.distance
    related_org = related_org.organization
    storages = OrganizationStorageDist.objects.filter(
        organization=related_org).exclude(storage=org_stor)
    # response = OrganizationStorageDist.objects.create(
    #     organization=new_org, storage=org_stor, distance=dist)
    with transaction.atomic():
        OrganizationStorageDist.objects.bulk_create(
            OrganizationStorageDist(
                organization=new_org,
                storage=obj.storage,
                distance=dist + related_org_dist + obj.distance
            ) for obj in storages
        )
    # return response
