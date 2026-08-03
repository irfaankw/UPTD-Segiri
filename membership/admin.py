from django.contrib import admin
from .models import Anggota

@admin.register(Anggota)
class AnggotaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'pasar', 'urutan', 'jabatan', 'kategori')
    list_display_links = ('nama',)
    list_filter = ('kategori', 'pasar')
    search_fields = ('nama', 'jabatan', 'nip')
    list_editable = ('urutan', 'kategori')
    autocomplete_fields = ('pasar',)