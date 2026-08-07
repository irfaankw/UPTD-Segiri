from django.shortcuts import render, get_object_or_404
from .models import Anggota

def index(request):
    # 1. Pimpinan
    pimpinan_list = Anggota.objects.filter(kategori='pimpinan')
    
    # 2. Pengelola Kepala Unit (Staf yang memiliki relasi ke unit pasar)
    kepala_unit_list = Anggota.objects.filter(kategori='staf', pasar__isnull=False)
    
    # 3. Staf & Administrasi (Staf yang tidak terhubung ke unit pasar khusus)
    staf_list = Anggota.objects.filter(kategori='staf', pasar__isnull=True)
    
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