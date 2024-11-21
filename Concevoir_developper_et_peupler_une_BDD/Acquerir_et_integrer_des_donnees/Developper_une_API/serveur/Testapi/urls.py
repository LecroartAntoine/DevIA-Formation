from django.urls import path
from . import views

urlpatterns = [
    path('val', views.random_gen, name='Random'),
    path('calc/add', views.somme, name='Somme'),
    path('calc/prod', views.produit, name='Produit'),
    path('img', views.show_img, name='Image'),
    path('stations_velo', views.info_station, name='Station vélo'),
    path('stations_velo/<int:id>/<str:option>', views.info_station_option, name='Station vélo option'),
    path('stations_velo/toutes/cap', views.info_station_somme, name='Station vélo somme'),
    path('', views.index, name='index')
]