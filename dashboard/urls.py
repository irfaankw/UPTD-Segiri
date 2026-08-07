from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='dashboard/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', views.home_dashboard, name='home_dashboard'),
    path('cari/', views.pencarian, name='pencarian'),

    # Pengaduan
    path('pengaduan/', views.pengaduan_list, name='pengaduan_list'),
    path('pengaduan/<int:pk>/status/', views.pengaduan_update_status, name='pengaduan_update_status'),
    path('pengaduan/<int:pk>/hapus/', views.pengaduan_delete, name='pengaduan_delete'),

    # Unit Pasar
    path('unit-pasar/', views.unit_pasar_list, name='unit_pasar_list'),
    path('unit-pasar/tambah/', views.unit_pasar_create, name='unit_pasar_create'),
    path('unit-pasar/<int:pk>/edit/', views.unit_pasar_update, name='unit_pasar_update'),
    path('unit-pasar/<int:pk>/hapus/', views.unit_pasar_delete, name='unit_pasar_delete'),

    # Anggota
    path('anggota/', views.anggota_list, name='anggota_list'),
    path('anggota/tambah/', views.anggota_create, name='anggota_create'),
    path('anggota/<int:pk>/edit/', views.anggota_update, name='anggota_update'),
    path('anggota/<int:pk>/hapus/', views.anggota_delete, name='anggota_delete'),

    # Galeri
    path('galeri/', views.gallery_list, name='gallery_list'),
    path('galeri/tambah/', views.gallery_create, name='gallery_create'),
    path('galeri/<int:pk>/hapus/', views.gallery_delete, name='gallery_delete'),
    path("galeri/<int:pk>/edit/", views.gallery_edit, name="gallery_edit"),

    # Profil UPTD
    path('profil-uptd/', views.profil_uptd, name='profil_uptd'),
    path('profil-uptd/misi/tambah/', views.misi_tambah, name='misi_tambah'),
    path('profil-uptd/misi/<int:pk>/hapus/', views.misi_hapus, name='misi_hapus'),
]