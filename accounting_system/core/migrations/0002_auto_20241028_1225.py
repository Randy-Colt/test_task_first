# Generated by Django 3.2.3 on 2024-10-28 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationstoragedist',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storages', to='core.organization', verbose_name='Организация'),
        ),
        migrations.AlterField(
            model_name='organizationstoragedist',
            name='storage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to='core.storage', verbose_name='Хранилище'),
        ),
    ]
