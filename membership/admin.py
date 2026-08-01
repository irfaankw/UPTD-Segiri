from django.contrib import admin
from .models import Anggota

@admin.register(Anggota)
class AnggotaAdmin(admin.ModelAdmin):
    # Pindahkan 'nama' ke posisi pertama agar 'urutan' bisa di-edit langsung
    list_display = ('nama', 'urutan', 'jabatan', 'kategori')
    
    # Menentukan bahwa kolom 'nama' yang berfungsi sebagai link klik edit
    list_display_links = ('nama',)
    
    list_filter = ('kategori',)
    search_fields = ('nama', 'jabatan', 'nip')
    list_editable = ('urutan', 'kategori')