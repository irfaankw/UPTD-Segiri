from django.core.paginator import Paginator
from django.shortcuts import render
from market.models import Pasar  # <-- 1. TAMBAHKAN IMPORT INI
from membership.models import Anggota

from .models import Galeri, HeroBannerUtama, ProfilUPTD


def home(request):
    profil = ProfilUPTD.objects.first()
    galeri_preview = Galeri.objects.all()[:3]

    # Ambil maksimal 2 pimpinan dari app membership untuk tampilan beranda sejajar
    pimpinan_list = Anggota.objects.filter(kategori="pimpinan")[:2]

    # Ambil pimpinan utama (tetap dipertahankan untuk keamanan kompatibilitas)
    pimpinan_utama = pimpinan_list.first() if pimpinan_list else None

    # Ambil data hero banner utama
    hero_banner = HeroBannerUtama.objects.first()

    # <-- 2. TAMBAHKAN QUERY PASAR DI SINI (Ambil 3 pasar pertama)
    unit_pasar_list = Pasar.objects.all()[:3]

    context = {
        "title": "Beranda",
        "profil": profil,
        "galeri_preview": galeri_preview,
        "pimpinan_list": pimpinan_list,
        "pimpinan_utama": pimpinan_utama,
        "hero_banner": hero_banner,
        "unit_pasar_list": unit_pasar_list,  # <-- 3. MASUKKAN KE CONTEXT
    }
    return render(request, "core/home.html", context)


# --- FUNGSI DI BAWAH INI TIDAK DISENTUH ---


def uptd_profile(request):
    profil = ProfilUPTD.objects.first()
    pimpinan_list = Anggota.objects.filter(
        pasar__isnull=True, kategori="pimpinan"
    )
    staf_list = Anggota.objects.filter(pasar__isnull=True, kategori="staf")

    context = {
        "title": "Profil UPTD",
        "profil": profil,
        "pimpinan_list": pimpinan_list,
        "staf_list": staf_list,
    }
    return render(request, "core/uptd_profile.html", context)


def gallery(request):
    kategori_selected = request.GET.get("kategori", "kebersamaan")

    if kategori_selected in ["kebersamaan", "kegiatan"]:
        galeri_list = Galeri.objects.filter(kategori=kategori_selected)
    else:
        galeri_list = Galeri.objects.filter(kategori="kebersamaan")

    paginator = Paginator(galeri_list, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    total_pages = paginator.num_pages

    start_page = max(1, current_page - 4)
    end_page = min(total_pages, start_page + 9)
    if end_page - start_page < 9:
        start_page = max(1, end_page - 9)

    custom_page_range = range(start_page, end_page + 1)

    context = {
        "title": "Galeri",
        "page_obj": page_obj,
        "kategori_selected": kategori_selected,
        "custom_page_range": custom_page_range,
    }
    return render(request, "core/gallery.html", context)