from django.urls import path
from . import views

app_name = "complaint"
urlpatterns = [
    path("kirim/", views.submit_pengaduan, name="submit"),
]