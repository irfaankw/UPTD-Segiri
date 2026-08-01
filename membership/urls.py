from django.urls import path
from . import views

app_name = 'membership'

urlpatterns = [
    # Hubungkan ke views.index (bukan views.membership)
    path('', views.index, name='membership'),
    
    # Path untuk halaman detail
    path('<int:pk>/', views.detail_anggota, name='detail'),
]