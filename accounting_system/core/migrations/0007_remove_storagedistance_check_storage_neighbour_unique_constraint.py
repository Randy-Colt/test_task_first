# Generated by Django 3.2.3 on 2024-10-31 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20241031_1203'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='storagedistance',
            name='check_storage_neighbour_unique_constraint',
        ),
    ]
