from django.db.models import Min
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import OrganizationStorageDist, StorageDistance

@receiver(post_save, sender=StorageDistance)
def create_path_to_org(sender, instance, created, **kwargs):
    if created:
        neighbour_storage = instance.neighbour_storage
        inst_dist = instance.distance
        orgs_dist = OrganizationStorageDist.objects.filter(
            storage=instance.storage)
        OrganizationStorageDist.objects.bulk_create(
            OrganizationStorageDist(
                organization=item.organization,
                storage=neighbour_storage,
                distance=item.distance + inst_dist
            ) for item in orgs_dist
        )
