from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('core.urls', namespace='core')),
    path("unit-pasar/", include('market.urls', namespace='market')),
    path("keanggotaan/", include('membership.urls', namespace='membership')),
]