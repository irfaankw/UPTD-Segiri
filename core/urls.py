from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),
    path('profil-uptd/', views.uptd_profile, name='uptd_profile'),
    path('galeri/', views.gallery, name='gallery'),
]