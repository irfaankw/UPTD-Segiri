from django.shortcuts import render
from django.core.paginator import Paginator
from .models import ProfilUPTD, Galeri

def home(request):
    context = {
        'title' : 'Beranda',
        'isi' : 'Ini adalah halaman Beranda!',
    }
    return render(request, 'core/home.html', context)

def uptd_profile(request):
    profil = ProfilUPTD.objects.first()
    context = {
        'title': 'Profil UPTD',
        'profil': profil,
    }
    return render(request, 'core/uptd_profile.html', context)

def gallery(request):
    kategori_selected = request.GET.get('kategori', 'kebersamaan') # Default langsung ke Kebersamaan
    
    # Filter data berdasarkan kategori
    if kategori_selected in ['kebersamaan', 'kegiatan']:
        galeri_list = Galeri.objects.filter(kategori=kategori_selected)
    else:
        galeri_list = Galeri.objects.filter(kategori='kebersamaan')

    # 15 foto per halaman ( Grid 3x5 )
    paginator = Paginator(galeri_list, 15) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Batasi tampilan angka pagination hingga maksimal 10 halaman
    current_page = page_obj.number
    total_pages = paginator.num_pages
    
    start_page = max(1, current_page - 4)
    end_page = min(total_pages, start_page + 9)
    if end_page - start_page < 9:
        start_page = max(1, end_page - 9)
        
    custom_page_range = range(start_page, end_page + 1)

    context = {
        'title': 'Galeri',
        'page_obj': page_obj,
        'kategori_selected': kategori_selected,
        'custom_page_range': custom_page_range,
    }
    return render(request, 'core/gallery.html', context)