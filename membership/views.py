from django.shortcuts import render, get_object_or_404
from .models import Anggota

def index(request):
    pimpinan_list = Anggota.objects.filter(kategori='pimpinan')
    staf_list = Anggota.objects.filter(kategori='staf')
    return render(request, 'membership/membership.html', {
        'pimpinan_list': pimpinan_list,
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