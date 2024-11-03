# Generated by Django 3.2.3 on 2024-10-31 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20241029_1351'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='organizationstoragedist',
            constraint=models.UniqueConstraint(fields=('organization', 'storage'), name='check_org_storage_unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='storagedistance',
            constraint=models.UniqueConstraint(fields=('storage', 'neighbour_storage'), name='check_storage_neighbour_unique_constraint'),
        ),
    ]