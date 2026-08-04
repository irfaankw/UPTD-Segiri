from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify


def validate_video_size(file):
    """Batasi ukuran video maks 45MB (buffer aman dari limit bucket Supabase 50MB)."""
    max_mb = 45
    if file.size > max_mb * 1024 * 1024:
        raise ValidationError(
            f"Ukuran video maksimal {max_mb}MB (sekarang {file.size / 1024 / 1024:.1f}MB). "
            "Kompres dulu pakai HandBrake atau ffmpeg sebelum upload."
        )


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

    video_profil = models.FileField(
        upload_to="market/video/",
        blank=True, null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["mp4", "webm"]),
            validate_video_size,
        ],
        help_text="Upload video profil pasar ini (format MP4/WebM, maks 45MB). "
                   "Kompres dulu ke H.264 720p pakai HandBrake/ffmpeg sebelum upload. "
                   "Kosongkan jika belum ada video.",
    )
    video_thumbnail = models.ImageField(
        upload_to="market/video_thumbnail/",
        blank=True, null=True,
        help_text="Foto poster/thumbnail video (ditampilkan sebelum user klik play). "
                   "Jika kosong, akan pakai foto utama pasar sebagai fallback.",
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