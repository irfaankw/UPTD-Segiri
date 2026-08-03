from django.shortcuts import render, get_object_or_404
from .models import Pasar

def market_unit(request):
    daftar_pasar = Pasar.objects.all()
    context = {
        "title": "Unit Pasar",
        "daftar_pasar": daftar_pasar,
        "total_pasar": daftar_pasar.count(),
        "total_pedagang": sum(p.jumlah_pedagang for p in daftar_pasar),
    }
    return render(request, "market/market_unit.html", context)

def market_detail(request, slug):
    pasar = get_object_or_404(
        Pasar.objects.prefetch_related(
            "foto_aktivitas",
            "sarana_fasilitas",
            "komoditas_unggulan",
            "dokumen_resmi",
            "anggota",
        ),
        slug=slug,
    )
    context = {
        "title": pasar.nama,
        "pasar": pasar,
        "kepala_unit": pasar.anggota.first(),
    }
    return render(request, "market/market_detail.html", context)