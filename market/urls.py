from django.urls import path
from . import views

app_name = "market"
urlpatterns = [
    path("", views.market_unit, name="market_unit"),
    path("<slug:slug>/", views.market_detail, name="market_detail"),
]