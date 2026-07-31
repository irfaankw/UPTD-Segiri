from django.shortcuts import render

def home(request):
    context = {
        'title' : 'Beranda',
        'isi' : 'Ini adalah halaman Beranda!',
    }
    return render(request, 'core/home.html', context)

def uptd_profile(request):
    context = {
        'title' : 'Profil UPTD',
    }
    return render(request, 'core/uptd_profile.html', context)

def gallery(request):
    context = {
        'title' : 'Galeri',
    }
    return render(request, 'core/gallery.html', context)