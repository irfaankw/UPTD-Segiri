from django.urls import path
from . import views

app_name = "market"
urlpatterns = [
    path("", views.market_unit, name="market_unit"),
    path("dokumen/<int:pk>/lihat/", views.dokumen_lihat, name="dokumen_lihat"),
    path("dokumen/<int:pk>/unduh/", views.dokumen_unduh, name="dokumen_unduh"),
    path("<slug:slug>/", views.market_detail, name="market_detail"),
]