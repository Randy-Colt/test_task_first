from django.urls import include, path

from api import views

urlpatterns = [
    path('storages/', views.get_storages, name='storages_list'),
    path('create-org/', views.create_organization, name='create_org'),
    path('distance/', views.add_storage_dist, name='add_org_stor_dist'),
    path('dumping/', views.send_waste, name='dumping_waste'),
    path('stock/', views.refil_or_check_org_stock, name='refil_check_stock'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
