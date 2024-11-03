from django.urls import include, path

from . import views

urlpatterns = [
    path('storages/', views.get_storages, name='storages_list'),
    path('create-org/', views.create_organization, name='create_org'),
    path('add-storage/', views.add_storage, name='add_org_storage_dist'),
    path('dumping/', views.send_waste, name='dumping_waste'),
    path('auth/', include('djoser.urls.authtoken'))
]
