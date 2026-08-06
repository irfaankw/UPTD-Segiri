from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path(settings.ADMIN_PATH, include('dashboard.urls', namespace='dashboard')),
    path("", include('core.urls', namespace='core')),
    path("unit-pasar/", include('market.urls', namespace='market')),
    path("keanggotaan/", include('membership.urls', namespace='membership')),
    path('pengaduan/', include('complaint.urls', namespace='complaint'))
]