from django.db import models


class Pengaduan(models.Model):
    KATEGORI_CHOICES = [
        ("saran", "Saran"),
        ("masukan", "Masukan"),
        ("fasilitas", "Fasilitas"),
        ("kebersihan", "Kebersihan"),
        ("keamanan", "Keamanan"),
        ("lainnya", "Lainnya"),
    ]
    STATUS_CHOICES = [
        ("baru", "Baru"),
        ("diproses", "Diproses"),
        ("selesai", "Selesai"),
    ]

    nama = models.CharField(max_length=150, blank=True, default="Anonim")
    telepon = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES)
    kategori_lainnya = models.CharField(
        max_length=100, blank=True,
        help_text="Diisi hanya jika kategori = 'Lainnya'"
    )
    pesan = models.TextField()
    lampiran = models.FileField(upload_to="pengaduan/lampiran/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="baru")
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-dibuat_pada"]
        verbose_name = "Pengaduan"
        verbose_name_plural = "Pengaduan & Masukan"

    def kategori_display(self):
        """Label kategori untuk ditampilkan di admin, termasuk teks custom jika 'Lainnya'."""
        if self.kategori == "lainnya" and self.kategori_lainnya:
            return f"Lainnya: {self.kategori_lainnya}"
        return self.get_kategori_display()

    def __str__(self):
        return f"{self.nama} - {self.kategori_display()} ({self.dibuat_pada:%d %b %Y})"