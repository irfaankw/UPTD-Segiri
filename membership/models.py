from django.db import models

class Anggota(models.Model):
    KATEGORI_CHOICES = (
        ('pimpinan', 'Pimpinan'),
        ('staf', 'Staf & Koordinator Lapangan'),
    )

    nama = models.CharField(max_length=100)
    jabatan = models.CharField(max_length=100)
    nip = models.CharField(max_length=30, blank=True, null=True)
    foto = models.ImageField(upload_to='anggota/', blank=True, null=True)
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES)
    email = models.EmailField(blank=True, null=True)
    masa_jabatan = models.CharField(max_length=50, blank=True, null=True, help_text="Contoh: 2022 - Sekarang")
    uraian_tugas = models.TextField(blank=True, null=True, help_text="Penjelasan detail uraian tugas anggota")
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['urutan']

    def __str__(self):
        return f"{self.nama} - {self.jabatan}"