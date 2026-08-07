import mimetypes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models
from django.db.models.functions import Lower, Trim
from django.core.paginator import Paginator

from .decorators import staff_required
from .forms import PasarForm, AnggotaForm, GaleriForm, ProfilUPTDForm, MisiUPTDForm
from django import forms
from django.forms import inlineformset_factory
from urllib.parse import urlencode
from django.core.paginator import Paginator
from django.http import FileResponse, Http404
from market.models import (
    Pasar, FotoAktivitasPasar, SaranaFasilitas, KomoditasUnggulan, DokumenResmi,
)

from complaint.models import Pengaduan
from market.models import Pasar
from membership.models import Anggota
from core.models import Galeri, ProfilUPTD, MisiUPTD


# ---------- DASHBOARD HOME ----------
@staff_required
def home_dashboard(request):
    pasar_qs = Pasar.objects.all()

    total_pengaduan = Pengaduan.objects.count()
    status_baru = Pengaduan.objects.filter(status="baru").count()
    status_diproses = Pengaduan.objects.filter(status="diproses").count()
    status_selesai = Pengaduan.objects.filter(status="selesai").count()

    kategori_counts = (
        Pengaduan.objects.values("kategori")
        .annotate(count=models.Count("id"))
        .order_by("-count")
    )
    kategori_label_map = dict(Pengaduan.KATEGORI_CHOICES)
    max_kategori = max([k["count"] for k in kategori_counts], default=0)
    kategori_breakdown = [
        {
            "label": kategori_label_map.get(k["kategori"], k["kategori"]),
            "count": k["count"],
            "percent": round((k["count"] / max_kategori) * 100) if max_kategori else 0,
        }
        for k in kategori_counts
    ]

    context = {
        "total_pasar": pasar_qs.count(),
        "total_pedagang": sum(p.jumlah_pedagang for p in pasar_qs),
        "total_anggota": Anggota.objects.count(),
        "total_pengaduan": total_pengaduan,
        "pengaduan_pending": status_baru,

        # dikonsumsi via json_script di template, dibaca sama home_charts.js
        "pasar_labels": [p.nama for p in pasar_qs],
        "pasar_data": [p.jumlah_pedagang for p in pasar_qs],
        "status_chart": {"selesai": status_selesai, "diproses": status_diproses, "baru": status_baru},

        # dipakai buat teks di template (badge, legend, dst)
        "status_baru": status_baru,
        "status_diproses": status_diproses,
        "status_selesai": status_selesai,

        "kategori_breakdown": kategori_breakdown,
        "pengaduan_terbaru": Pengaduan.objects.all()[:5],
    }
    return render(request, "dashboard/home_dashboard.html", context)

# ---------- PENGADUAN ----------
def _build_page_range(current, total, window=2):
    """Bikin daftar nomor halaman + None (buat elipsis '...') di komponen paginasi."""
    pages = sorted(set([1, total] + list(range(max(1, current - window), min(total, current + window) + 1))))
    result = []
    last = 0
    for p in pages:
        if last and p - last > 1:
            result.append(None)
        result.append(p)
        last = p
    return result

@staff_required
def pengaduan_list(request):
    semua_pengaduan = Pengaduan.objects.all()

    pengaduan = semua_pengaduan
    status_filter = request.GET.get("status")
    if status_filter:
        pengaduan = pengaduan.filter(status=status_filter)

    dari = request.GET.get("dari", "")
    sampai = request.GET.get("sampai", "")
    if dari:
        pengaduan = pengaduan.filter(dibuat_pada__date__gte=dari)
    if sampai:
        pengaduan = pengaduan.filter(dibuat_pada__date__lte=sampai)

    paginator = Paginator(pengaduan, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    querystring = request.GET.copy()
    querystring.pop("page", None)

    date_params = {}
    if dari:
        date_params["dari"] = dari
    if sampai:
        date_params["sampai"] = sampai

    context = {
        "pengaduan_list": page_obj,
        "page_obj": page_obj,
        "page_range": _build_page_range(page_obj.number, paginator.num_pages),
        "status_choices": Pengaduan.STATUS_CHOICES,
        "status_filter": status_filter,
        "dari": dari,
        "sampai": sampai,
        "querystring": querystring.urlencode(),
        "date_query": urlencode(date_params),
        "total_pengaduan": semua_pengaduan.count(),
        "count_baru": semua_pengaduan.filter(status="baru").count(),
        "count_diproses": semua_pengaduan.filter(status="diproses").count(),
        "count_selesai": semua_pengaduan.filter(status="selesai").count(),
    }
    return render(request, "dashboard/complaint_list.html", context)

@staff_required
def pengaduan_update_status(request, pk):
    item = get_object_or_404(Pengaduan, pk=pk)
    if request.method == "POST":
        status_baru = request.POST.get("status")
        if status_baru in dict(Pengaduan.STATUS_CHOICES):
            item.status = status_baru
            item.save()
            messages.success(request, f"Status pengaduan dari {item.nama} diupdate.")
    return redirect("dashboard:pengaduan_list")

@staff_required
def pengaduan_delete(request, pk):
    item = get_object_or_404(Pengaduan, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Pengaduan dihapus.")
    return redirect("dashboard:pengaduan_list")

@staff_required
def pengaduan_lampiran_lihat(request, pk):
    pengaduan = get_object_or_404(Pengaduan, pk=pk)
    if not pengaduan.lampiran:
        raise Http404("Lampiran tidak ditemukan.")
    content_type, _ = mimetypes.guess_type(pengaduan.lampiran.name)
    try:
        return FileResponse(
            pengaduan.lampiran.open("rb"),
            content_type=content_type or "application/octet-stream",
        )
    except FileNotFoundError:
        raise Http404("Lampiran tidak ditemukan.")

# ---------- UNIT PASAR ----------
FotoAktivitasFormSet = inlineformset_factory(
    Pasar, FotoAktivitasPasar,
    fields=["gambar", "keterangan", "urutan"],
    extra=1, can_delete=True,
    widgets={
        "gambar": forms.FileInput(attrs={"class": "adm-file-input", "accept": "image/*"}),
        "keterangan": forms.TextInput(attrs={"class": "adm-field", "placeholder": "Keterangan singkat foto"}),
        "urutan": forms.NumberInput(attrs={"class": "adm-field"}),
    },
)
SaranaFasilitasFormSet = inlineformset_factory(
    Pasar, SaranaFasilitas,
    fields=["nama", "urutan"],
    extra=1, can_delete=True,
    widgets={
        "nama": forms.TextInput(attrs={"class": "adm-field", "placeholder": "Nama sarana/fasilitas"}),
        "urutan": forms.NumberInput(attrs={"class": "adm-field"}),
    },
)
KomoditasUnggulanFormSet = inlineformset_factory(
    Pasar, KomoditasUnggulan,
    fields=["nama", "urutan"],
    extra=1, can_delete=True,
    widgets={
        "nama": forms.TextInput(attrs={"class": "adm-field", "placeholder": "Nama komoditas"}),
        "urutan": forms.NumberInput(attrs={"class": "adm-field"}),
    },
)
DokumenResmiFormSet = inlineformset_factory(
    Pasar, DokumenResmi,
    fields=["judul", "file", "urutan"],
    extra=1, can_delete=True,
    widgets={
        "judul": forms.TextInput(attrs={"class": "adm-field", "placeholder": "Judul dokumen"}),
        "file": forms.FileInput(attrs={"class": "adm-file-input", "accept": "application/pdf"}),
        "urutan": forms.NumberInput(attrs={"class": "adm-field"}),
    },
)

@staff_required
def unit_pasar_list(request):
    pasar_list = list(Pasar.objects.all())
    context = {
        "pasar_list": pasar_list,
        "total_pasar": len(pasar_list),
        "total_pedagang": sum(p.jumlah_pedagang for p in pasar_list),
        "total_video": sum(1 for p in pasar_list if p.video_profil),
        "belum_lengkap": sum(1 for p in pasar_list if not p.foto or not p.video_profil),
    }
    return render(request, "dashboard/market_list.html", context)


def _build_pasar_formsets(request, pasar=None):
    """Helper biar create & update gak duplikat kode instansiasi formset."""
    post = request.POST or None
    files = request.FILES or None
    return {
        "foto_formset": FotoAktivitasFormSet(post, files, instance=pasar, prefix="foto"),
        "sarana_formset": SaranaFasilitasFormSet(post, instance=pasar, prefix="sarana"),
        "komoditas_formset": KomoditasUnggulanFormSet(post, instance=pasar, prefix="komoditas"),
        "dokumen_formset": DokumenResmiFormSet(post, files, instance=pasar, prefix="dokumen"),
    }


@staff_required
def unit_pasar_create(request):
    form = PasarForm(request.POST or None, request.FILES or None)
    formsets = _build_pasar_formsets(request)

    if request.method == "POST":
        if form.is_valid() and all(fs.is_valid() for fs in formsets.values()):
            pasar = form.save()
            for fs in formsets.values():
                fs.instance = pasar
                fs.save()
            messages.success(request, "Unit pasar berhasil ditambahkan.")
            return redirect("dashboard:unit_pasar_list")
        messages.error(request, "Ada isian yang belum valid, silakan cek kembali form di bawah.")

    context = {"form": form, "mode": "tambah", **formsets}
    return render(request, "dashboard/market_form.html", context)


@staff_required
def unit_pasar_update(request, pk):
    pasar = get_object_or_404(Pasar, pk=pk)
    form = PasarForm(request.POST or None, request.FILES or None, instance=pasar)
    formsets = _build_pasar_formsets(request, pasar=pasar)

    if request.method == "POST":
        if form.is_valid() and all(fs.is_valid() for fs in formsets.values()):
            form.save()
            for fs in formsets.values():
                fs.save()
            messages.success(request, "Unit pasar berhasil diperbarui.")
            return redirect("dashboard:unit_pasar_list")
        messages.error(request, "Ada isian yang belum valid, silakan cek kembali form di bawah.")

    context = {"form": form, "mode": "edit", "pasar": pasar, **formsets}
    return render(request, "dashboard/market_form.html", context)


@staff_required
def unit_pasar_delete(request, pk):
    pasar = get_object_or_404(Pasar, pk=pk)
    if request.method == "POST":
        pasar.delete()
        messages.success(request, "Unit pasar dihapus.")
    return redirect("dashboard:unit_pasar_list")


# ---------- ANGGOTA ----------
@staff_required
def anggota_list(request):
    return render(request, "dashboard/member_list.html", {"anggota_list": Anggota.objects.all()})

@staff_required
def anggota_create(request):
    form = AnggotaForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Anggota berhasil ditambahkan.")
        return redirect("dashboard:anggota_list")
    return render(request, "dashboard/member_form.html", {"form": form, "mode": "tambah"})

@staff_required
def anggota_update(request, pk):
    anggota = get_object_or_404(Anggota, pk=pk)
    form = AnggotaForm(request.POST or None, request.FILES or None, instance=anggota)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Anggota berhasil diperbarui.")
        return redirect("dashboard:anggota_list")
    return render(request, "dashboard/member_form.html", {"form": form, "mode": "edit", "anggota": anggota})

@staff_required
def anggota_delete(request, pk):
    anggota = get_object_or_404(Anggota, pk=pk)
    if request.method == "POST":
        anggota.delete()
        messages.success(request, "Anggota dihapus.")
    return redirect("dashboard:anggota_list")


# ---------- GALERI ----------
@staff_required
def gallery_list(request):
    selected_category = request.GET.get('kategori', '').strip()
    
    if selected_category:
        galleries = Galeri.objects.filter(kategori__icontains=selected_category).order_by('-tanggal')
    else:
        galleries = Galeri.objects.all().order_by('-tanggal')
    
    categories = ['kebersamaan', 'kegiatan']

    paginator = Paginator(galleries, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'gallery_list': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, "dashboard/gallery_list.html", context)

@staff_required
def gallery_create(request):
    form = GaleriForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        galeri = form.save(commit=False)
        if galeri.kategori:
            galeri.kategori = galeri.kategori.strip()
        galeri.save()
        messages.success(request, "Foto berhasil ditambahkan ke galeri.")
        return redirect("dashboard:gallery_list")
    return render(request, "dashboard/gallery_form.html", {"form": form})

@staff_required
def gallery_edit(request, pk):
    foto = get_object_or_404(Galeri, pk=pk)
    form = GaleriForm(request.POST or None, request.FILES or None, instance=foto)
    if request.method == 'POST' and form.is_valid():
        galeri = form.save(commit=False)
        if galeri.kategori:
            galeri.kategori = galeri.kategori.strip()
        galeri.save()
        messages.success(request, 'Data galeri berhasil diperbarui!')
        return redirect('dashboard:gallery_list')
    return render(request, 'dashboard/gallery_form.html', {'form': form})

@staff_required
def gallery_delete(request, pk):
    foto = get_object_or_404(Galeri, pk=pk)
    if request.method == "POST":
        foto.delete()
        messages.success(request, "Foto dihapus dari galeri.")
    return redirect("dashboard:gallery_list")


# ---------- PROFIL UPTD ----------
@staff_required
def profil_uptd(request):
    profil, _ = ProfilUPTD.objects.get_or_create(pk=1, defaults={
        "sambutan_isi": "",
        "nama_kepala": "",
        "visi": "",
        "alamat": "",
        "google_maps_embed_url": "",
        "google_maps_link": "",
    })
    form = ProfilUPTDForm(request.POST or None, request.FILES or None, instance=profil)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profil UPTD berhasil disimpan.")
        return redirect("dashboard:profil_uptd")

    context = {
        "form": form,
        "misi_list": profil.misi_list.all(),
        "misi_form": MisiUPTDForm(),
    }
    return render(request, "dashboard/profile.html", context)

@staff_required
def misi_tambah(request):
    if request.method == "POST":
        form = MisiUPTDForm(request.POST)
        if form.is_valid():
            profil, _ = ProfilUPTD.objects.get_or_create(pk=1)
            urutan_terakhir = profil.misi_list.count() + 1
            misi = form.save(commit=False)
            misi.profil = profil
            misi.urutan = urutan_terakhir
            misi.save()
            messages.success(request, "Misi ditambahkan.")
        else:
            messages.error(request, "Isi misi tidak boleh kosong.")
    return redirect("dashboard:profil_uptd")

@staff_required
def misi_hapus(request, pk):
    misi = get_object_or_404(MisiUPTD, pk=pk)
    if request.method == "POST":
        misi.delete()
        messages.success(request, "Misi dihapus.")
    return redirect("dashboard:profil_uptd")

@staff_required
def pencarian(request):
    q = request.GET.get('q', '').strip()
    hasil = {}
    if q:
        hasil['pasar'] = Pasar.objects.filter(nama__icontains=q)
        hasil['anggota'] = Anggota.objects.filter(nama__icontains=q)
        hasil['pengaduan'] = Pengaduan.objects.filter(
            models.Q(nama__icontains=q) | models.Q(pesan__icontains=q)
        )
        hasil['galeri'] = Galeri.objects.filter(judul__icontains=q)

    total_hasil = sum(len(v) for v in hasil.values()) if q else 0
    context = {"q": q, "hasil": hasil, "total_hasil": total_hasil}
    return render(request, "dashboard/search_results.html", context)