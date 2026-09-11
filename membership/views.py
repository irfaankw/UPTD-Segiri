from django.shortcuts import render, get_object_or_404
from django.db.models import Q  # Import Q untuk query kombinasi OR
from .models import Anggota

def index(request):
    # 1. Pimpinan
    pimpinan_list = Anggota.objects.filter(kategori='pimpinan')
    
    # 2. Pengelola Kepala Unit:
    # Mengambil staf yang punya relasi ke pasar ATAU jabatannya mengandung kata "kepala" / "pengelola"
    kepala_unit_list = Anggota.objects.filter(
        kategori='staf'
    ).filter(
        Q(pasar__isnull=False) | 
        Q(jabatan__icontains='kepala') | 
        Q(jabatan__icontains='pengelola')
    ).distinct()
    
    # 3. Staf & Administrasi:
    # Mengambil staf selain yang sudah masuk ke daftar kepala_unit_list di atas
    staf_list = Anggota.objects.filter(kategori='staf').exclude(
        pk__in=kepala_unit_list.values_list('pk', flat=True)
    )
    
    return render(request, 'membership/membership.html', {
        'pimpinan_list': pimpinan_list,
        'kepala_unit_list': kepala_unit_list,
        'staf_list': staf_list
    })

def detail_anggota(request, pk):
    member = get_object_or_404(Anggota, pk=pk)
    # Mengambil anggota lainnya (selain anggota yang sedang dibuka)
    anggota_lainnya = Anggota.objects.exclude(pk=pk)[:4]
    
    context = {
        'member': member,
        'anggota_lainnya': anggota_lainnya,
    }
    return render(request, 'membership/member_detail.html', context)