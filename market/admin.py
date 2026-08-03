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

    fieldsets = (
        ("Informasi Dasar", {
            "fields": ("nama", "slug", "alamat", "foto", "kelas", "jam_operasional", "jumlah_pedagang", "urutan")
        }),
        ("Konten Halaman Detail", {
            "fields": ("deskripsi", "video_youtube_url", "sejarah_fungsi", "ekosistem_pedagang")
        }),
        ("Lokasi", {
            "fields": ("google_maps_embed_url", "google_maps_link")
        }),
        ("Struktur Organisasi", {
            "fields": ("struktur_organisasi_image",)
        }),
    )

    inlines = [FotoAktivitasInline, SaranaFasilitasInline, KomoditasUnggulanInline, DokumenResmiInline]