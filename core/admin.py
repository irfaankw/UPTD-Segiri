from django.contrib import admin
from .models import HeroBannerUtama, ProfilUPTD, MisiUPTD, Galeri

@admin.register(HeroBannerUtama)
class HeroBannerUtamaAdmin(admin.ModelAdmin):
    # Hanya tampilkan kolom yang ada
    list_display = ('__str__', 'gambar')

    # Mencegah penambahan data baru jika sudah ada 1 data (Singleton)
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    # Mencegah data terhapus
    def has_delete_permission(self, request, obj=None):
        return False

# ==========================================
# ADMIN SEBELUMNYA (TIDAK ADA YANG DIUBAH)
# ==========================================

class MisiInline(admin.TabularInline):
    model = MisiUPTD
    extra = 1
    max_num = 5

@admin.register(ProfilUPTD)
class ProfilUPTDAdmin(admin.ModelAdmin):
    inlines = [MisiInline]

    def has_add_permission(self, request):
        # Cegah bikin lebih dari 1 data (singleton)
        return not ProfilUPTD.objects.exists()

@admin.register(Galeri)
class GaleriAdmin(admin.ModelAdmin):
    list_display = ('judul', 'kategori', 'tanggal')
    list_filter = ('kategori', 'tanggal')
    search_fields = ('judul', 'keterangan')