from django.db import models

class ProfilUPTD(models.Model):
    # Sambutan Pimpinan
    sambutan_judul = models.CharField(
        max_length=200,
        default="Mewujudkan Pasar Segiri sebagai Pusat Ekonomi Rakyat yang Nyaman dan Modern",
        help_text="Judul/tagline sambutan pimpinan"
    )
    sambutan_isi = models.TextField(help_text="Isi lengkap sambutan pimpinan")
    nama_kepala = models.CharField(max_length=100)
    jabatan_kepala = models.CharField(max_length=150, default="Kepala UPTD Pasar Segiri")
    foto_kepala = models.ImageField(upload_to="profil/", blank=True, null=True)

    # Visi
    visi = models.TextField(help_text="Kalimat visi, tanpa perlu tanda kutip")

    # Struktur Organisasi
    struktur_organisasi = models.ImageField(
        upload_to="profil/", blank=True, null=True,
        help_text="Gambar bagan struktur organisasi"
    )

    # Lokasi
    alamat = models.TextField()
    google_maps_embed_url = models.URLField(
        max_length=500,
        help_text="URL src dari iframe embed Google Maps (Share > Embed a map)"
    )
    google_maps_link = models.URLField(
        max_length=500,
        help_text="Link biasa Google Maps (buat tombol 'Buka di Google Maps')"
    )

    # Jam Operasional
    jam_senin_kamis = models.CharField(max_length=50, default="07.30 - 14.30")
    jam_jumat = models.CharField(max_length=50, default="07.30 - 11.30")
    jam_sabtu = models.CharField(max_length=50, default="07.30 - 13.00")
    jam_minggu = models.CharField(max_length=50, default="Libur")

    class Meta:
        verbose_name = "Profil UPTD"
        verbose_name_plural = "Profil UPTD"

    def save(self, *args, **kwargs):
        # Singleton pattern — cuma boleh ada 1 baris data
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Cegah data ke-hapus gak sengaja

    def __str__(self):
        return "Profil UPTD Pasar Segiri"


class MisiUPTD(models.Model):
    profil = models.ForeignKey(ProfilUPTD, on_delete=models.CASCADE, related_name="misi_list")
    urutan = models.PositiveSmallIntegerField(default=1)
    isi = models.CharField(max_length=300)

    class Meta:
        ordering = ["urutan"]
        verbose_name = "Misi"
        verbose_name_plural = "Misi"

    def __str__(self):
        return f"{self.urutan}. {self.isi[:50]}"


# --- MODEL BARU: GALERI ---
class Galeri(models.Model):
    KATEGORI_CHOICES = [
        ('kebersamaan', 'Kebersamaan'),
        ('kegiatan', 'Kegiatan'),
    ]

    judul = models.CharField(max_length=200, help_text="Judul singkat foto")
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES)
    foto = models.ImageField(upload_to='galeri/')
    keterangan = models.TextField(blank=True, null=True)
    tanggal = models.DateField()

    class Meta:
        ordering = ['-tanggal']
        verbose_name = "Galeri"
        verbose_name_plural = "Galeri"

    def __str__(self):
        return f"{self.judul} - {self.get_kategori_display()}"


class HeroBannerUtama(models.Model):
    gambar = models.ImageField(
        upload_to='hero_banners/',
        blank=True,
        null=True,
        help_text="Gambar Banner Utama (Slide 1 Beranda)"
    )

    class Meta:
        verbose_name = "Hero Banner Utama"
        verbose_name_plural = "Hero Banner Utama"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def __str__(self):
        return "Hero Banner Utama"