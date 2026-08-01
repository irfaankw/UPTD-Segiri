from django.contrib import admin
from .models import Pengaduan

@admin.register(Pengaduan)
class PengaduanAdmin(admin.ModelAdmin):
    list_display = ("nama", "kategori_display", "status", "dibuat_pada")
    list_filter = ("kategori", "status", "dibuat_pada")
    search_fields = ("nama", "email", "telepon", "pesan", "kategori_lainnya")
    list_editable = ("status",)
    readonly_fields = ("dibuat_pada",)
    ordering = ("-dibuat_pada",)

    @admin.display(description="Kategori")
    def kategori_display(self, obj):
        return obj.kategori_display()