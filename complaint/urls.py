from django.urls import path
from . import views

app_name = "pengaduan"
urlpatterns = [
    path("kirim/", views.submit_pengaduan, name="submit"),
]