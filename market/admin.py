from django.contrib import admin
from .models import Pasar, FotoAktivitasPasar, SaranaFasilitas, KomoditasUnggulan, DokumenResmi

class FotoAktivitasInline(admin.TabularInline):
    model = FotoAktivitasPasar
    extra = 1
    fields = ["gambar", "keterangan", "urutan"]

class SaranaFasilitasInline(admin.TabularInline):
    model = SaranaFasilitas
    extra = 1
    fields = ["nama", "urutan"]

class KomoditasUnggulanInline(admin.TabularInline):
    model = KomoditasUnggulan
    extra = 1
    fields = ["nama", "urutan"]

class DokumenResmiInline(admin.TabularInline):
    model = DokumenResmi
    extra = 1
    fields = ["judul", "file", "urutan"]

@admin.register(Pasar)
class PasarAdmin(admin.ModelAdmin):
    list_display = ["nama", "kelas", "jumlah_pedagang", "urutan"]
    list_editable = ["urutan"]
    prepopulated_fields = {"slug": ("nama",)}
    search_fields = ["nama", "alamat"]

    ("Konten Halaman Detail", {
            "fields": ("deskripsi", "video_profil", "video_thumbnail", "sejarah_fungsi", "ekosistem_pedagang")
        }),

    inlines = [FotoAktivitasInline, SaranaFasilitasInline, KomoditasUnggulanInline, DokumenResmiInline]