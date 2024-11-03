# Generated by Django 3.2.3 on 2024-11-01 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_storagedistance_check_storage_neighbour_unique_constraint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waste',
            name='biowaste',
            field=models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Биоотходы'),
        ),
        migrations.AlterField(
            model_name='waste',
            name='glass',
            field=models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Стекло'),
        ),
        migrations.AlterField(
            model_name='waste',
            name='plastic',
            field=models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Пластик'),
        ),
    ]
