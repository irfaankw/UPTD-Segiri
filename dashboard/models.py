from django.db import models
from django.utils.text import slugify


class Pasar(models.Model):
    nama = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    alamat = models.TextField()
    foto = models.ImageField(upload_to='market/foto/', blank=True, null=True)
    jumlah_pedagang = models.PositiveIntegerField(default=0)
    kelas = models.CharField(max_length=50)
    jam_operasional = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    urutan = models.IntegerField(default=0)
    
    # PERUBAHAN DI SINI: Gunakan CharField untuk menyimpan Video ID YouTube (11 Karakter)
    video_profil = models.CharField(max_length=100, blank=True, null=True, help_text="ID atau URL Video YouTube")
    video_thumbnail = models.ImageField(upload_to='market/video_thumbs/', blank=True, null=True)
    
    sejarah_fungsi = models.TextField(blank=True, null=True)
    ekosistem_pedagang = models.TextField(blank=True, null=True)
    google_maps_embed_url = models.URLField(max_length=500, blank=True, null=True)
    google_maps_link = models.URLField(max_length=500, blank=True, null=True)
    struktur_organisasi_image = models.ImageField(upload_to='market/struktur/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama