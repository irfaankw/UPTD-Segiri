from django.db import models
from django.utils.text import slugify
from urllib.parse import urlparse, parse_qs

class Pasar(models.Model):
    KELAS_CHOICES = [
        ("A", "Tipe A"),
        ("B", "Tipe B"),
        ("C", "Tipe C"),
    ]

    nama = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    alamat = models.TextField()
    foto = models.ImageField(upload_to="market/foto/", blank=True, null=True)

    jumlah_pedagang = models.PositiveIntegerField(
        default=0,
        help_text="Update manual sesuai data rekap terbaru (bulanan/tahunan). "
                   "Merepresentasikan pedagang TERDAFTAR, bukan status kehadiran aktif harian.",
    )
    kelas = models.CharField(max_length=1, choices=KELAS_CHOICES, blank=True)
    jam_operasional = models.CharField(max_length=100, blank=True, default="06.00 - 18.00 WITA")
    deskripsi = models.TextField(blank=True, help_text="Opsional, paragraf penjelasan singkat tentang pasar ini.")
    urutan = models.PositiveSmallIntegerField(default=0, help_text="Urutan tampil di halaman daftar (kecil di depan).")

    # --- Bagian baru untuk market_detail.html ---

    video_youtube_url = models.URLField(
        blank=True,
        help_text="Tempel URL video YouTube (contoh: https://www.youtube.com/watch?v=XXXXXXXXXXX). "
                   "Kosongkan jika belum ada video profil pasar ini.",
    )

    sejarah_fungsi = models.TextField(
        blank=True, help_text="Paragraf 'Sejarah & Fungsi' pada halaman detail."
    )
    ekosistem_pedagang = models.TextField(
        blank=True, help_text="Paragraf 'Ekosistem Pedagang' pada halaman detail."
    )

    google_maps_embed_url = models.URLField(
        max_length=500, blank=True,
        help_text="URL embed dari Google Maps (Share > Embed a map > src iframe)."
    )
    google_maps_link = models.URLField(
        blank=True, help_text="Link 'Buka Google Maps' (link biasa, bukan embed)."
    )

    struktur_organisasi_image = models.ImageField(
        upload_to="market/struktur/", blank=True, null=True,
        help_text="Gambar bagan struktur organisasi unit pasar ini.",
    )

    class Meta:
        ordering = ["urutan", "nama"]
        verbose_name = "Unit Pasar"
        verbose_name_plural = "Unit Pasar"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama

    @property
    def youtube_video_id(self):
        """Ekstrak video ID dari berbagai format URL YouTube."""
        if not self.video_youtube_url:
            return ""
        try:
            parsed = urlparse(self.video_youtube_url)
            host = parsed.netloc.lower().replace("www.", "").replace("m.", "")

            if host == "youtu.be":
                return parsed.path.lstrip("/").split("/")[0]

            if "youtube.com" in host:
                if parsed.path == "/watch":
                    video_id = parse_qs(parsed.query).get("v", [""])[0]
                    return video_id
                for prefix in ("/embed/", "/shorts/", "/live/"):
                    if parsed.path.startswith(prefix):
                        return parsed.path[len(prefix):].split("/")[0]
        except Exception:
            return ""
        return ""

class FotoAktivitasPasar(models.Model):
    pasar = models.ForeignKey(Pasar, on_delete=models.CASCADE, related_name="foto_aktivitas")
    gambar = models.ImageField(upload_to="market/aktivitas/")
    keterangan = models.CharField(max_length=150, blank=True)
    urutan = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["urutan", "id"]
        verbose_name = "Foto Aktivitas Pasar"
        verbose_name_plural = "Foto Aktivitas Pasar"

    def __str__(self):
        return f"{self.pasar.nama} - Foto #{self.urutan}"

class SaranaFasilitas(models.Model):
    pasar = models.ForeignKey(Pasar, on_delete=models.CASCADE, related_name="sarana_fasilitas")
    nama = models.CharField(max_length=100)
    urutan = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["urutan", "id"]
        verbose_name = "Sarana & Fasilitas"
        verbose_name_plural = "Sarana & Fasilitas"

    def __str__(self):
        return f"{self.pasar.nama} - {self.nama}"

class KomoditasUnggulan(models.Model):
    pasar = models.ForeignKey(Pasar, on_delete=models.CASCADE, related_name="komoditas_unggulan")
    nama = models.CharField(max_length=100)
    urutan = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["urutan", "id"]
        verbose_name = "Komoditas Unggulan"
        verbose_name_plural = "Komoditas Unggulan"

    def __str__(self):
        return f"{self.pasar.nama} - {self.nama}"

class DokumenResmi(models.Model):
    pasar = models.ForeignKey(Pasar, on_delete=models.CASCADE, related_name="dokumen_resmi")
    judul = models.CharField(max_length=150)
    file = models.FileField(upload_to="market/dokumen/")
    urutan = models.PositiveSmallIntegerField(default=0)
    diunggah_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["urutan", "-diunggah_pada"]
        verbose_name = "Dokumen Resmi"
        verbose_name_plural = "Dokumen Resmi"

    def __str__(self):
        return f"{self.pasar.nama} - {self.judul}"