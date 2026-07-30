from django.shortcuts import render

def beranda(request):
    context = {
        'title' : 'Beranda',
        'isi' : 'Ini adalah halaman Beranda!',
    }
    return render(request, 'core/beranda.html', context)