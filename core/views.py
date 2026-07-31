from django.shortcuts import render
from .models import ProfilUPTD

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
    context = {
        'title' : 'Galeri',
    }
    return render(request, 'core/gallery.html', context)

    