from django import forms
from market.models import Pasar
from membership.models import Anggota
from core.models import Galeri, ProfilUPTD, MisiUPTD


class PasarForm(forms.ModelForm):
    class Meta:
        model = Pasar
        exclude = ["slug"]
        widgets = {
            "nama": forms.TextInput(attrs={"class": "adm-field"}),
            "alamat": forms.Textarea(attrs={"class": "adm-field", "rows": 3}),
            "foto": forms.FileInput(attrs={"class": "adm-file-input", "accept": "image/*"}),
            "jumlah_pedagang": forms.NumberInput(attrs={"class": "adm-field"}),
            "kelas": forms.Select(attrs={"class": "adm-field"}),
            "jam_operasional": forms.TextInput(attrs={"class": "adm-field"}),
            "deskripsi": forms.Textarea(attrs={"class": "adm-field", "rows": 4}),
            "urutan": forms.NumberInput(attrs={"class": "adm-field"}),
            "video_profil": forms.FileInput(attrs={"class": "adm-file-input", "accept": "video/mp4,video/webm"}),
            "video_thumbnail": forms.FileInput(attrs={"class": "adm-file-input", "accept": "image/*"}),
            "sejarah_fungsi": forms.Textarea(attrs={"class": "adm-field", "rows": 4}),
            "ekosistem_pedagang": forms.Textarea(attrs={"class": "adm-field", "rows": 4}),
            "google_maps_embed_url": forms.TextInput(attrs={"class": "adm-field"}),
            "google_maps_link": forms.TextInput(attrs={"class": "adm-field"}),
            "struktur_organisasi_image": forms.FileInput(attrs={"class": "adm-file-input", "accept": "image/*"}),
        }
        error_messages = {
            "nama": {"required": "Nama unit pasar tidak boleh kosong."},
            "alamat": {"required": "Alamat pasar tidak boleh kosong."},
        }


class AnggotaForm(forms.ModelForm):
    class Meta:
        model = Anggota
        fields = "__all__"
        widgets = {
            "nama": forms.TextInput(attrs={"class": "adm-field"}),
            "jabatan": forms.TextInput(attrs={"class": "adm-field"}),
            "kategori": forms.Select(attrs={"class": "adm-field"}),
            "pasar": forms.Select(attrs={"class": "adm-field"}),
            "masa_jabatan": forms.TextInput(attrs={"class": "adm-field"}),
            "sambutan_singkat": forms.Textarea(attrs={"class": "adm-field", "rows": 3}),
            "uraian_tugas": forms.Textarea(attrs={"class": "adm-field", "rows": 4}),
            "foto": forms.FileInput(attrs={"class": "adm-file-input"}),
        }
        error_messages = {
            "nama": {"required": "Nama anggota tidak boleh kosong."},
            "jabatan": {"required": "Jabatan tidak boleh kosong."},
            "kategori": {"required": "Silakan pilih salah satu kategori."},
        }


class GaleriForm(forms.ModelForm):
    class Meta:
        model = Galeri
        fields = "__all__"
        widgets = {
            "judul": forms.TextInput(attrs={"class": "adm-field"}),
            "kategori": forms.Select(attrs={"class": "adm-field"}),
            "keterangan": forms.Textarea(attrs={"class": "adm-field", "rows": 3}),
            "tanggal": forms.DateInput(attrs={"class": "adm-field", "type": "date"}),
            "foto": forms.FileInput(attrs={"class": "adm-file-input"}),
        }
        error_messages = {
            "judul": {"required": "Judul foto tidak boleh kosong."},
            "kategori": {"required": "Silakan pilih salah satu kategori."},
            "foto": {"required": "Silakan pilih foto untuk diunggah."},
            "tanggal": {"required": "Tanggal tidak boleh kosong."},
        }


class ProfilUPTDForm(forms.ModelForm):
    class Meta:
        model = ProfilUPTD
        exclude = []
        widgets = {
            "sambutan_judul": forms.TextInput(attrs={"class": "adm-field", "form": "profilForm"}),
            "sambutan_isi": forms.Textarea(attrs={"class": "adm-field", "rows": 5, "form": "profilForm"}),
            "nama_kepala": forms.TextInput(attrs={"class": "adm-field", "form": "profilForm"}),
            "jabatan_kepala": forms.TextInput(attrs={"class": "adm-field", "form": "profilForm"}),
            "foto_kepala": forms.FileInput(attrs={"class": "adm-file-input", "form": "profilForm"}),
            "visi": forms.Textarea(attrs={"class": "adm-field", "rows": 4, "form": "profilForm"}),
            "struktur_organisasi": forms.FileInput(attrs={"class": "adm-file-input", "form": "profilForm"}),
            "alamat": forms.Textarea(attrs={"class": "adm-field", "rows": 3, "form": "profilForm"}),
            "google_maps_embed_url": forms.TextInput(attrs={"class": "adm-field", "form": "profilForm"}),
            "google_maps_link": forms.TextInput(attrs={"class": "adm-field", "form": "profilForm"}),
            "jam_senin_kamis": forms.TextInput(attrs={"class": "adm-field", "form": "profilForm"}),
            "jam_jumat": forms.TextInput(attrs={"class": "adm-field", "form": "profilForm"}),
            "jam_sabtu": forms.TextInput(attrs={"class": "adm-field", "form": "profilForm"}),
            "jam_minggu": forms.TextInput(attrs={"class": "adm-field", "form": "profilForm"}),
        }
        error_messages = {
            "sambutan_judul": {"required": "Judul sambutan tidak boleh kosong."},
            "sambutan_isi": {"required": "Isi sambutan tidak boleh kosong."},
            "nama_kepala": {"required": "Nama kepala tidak boleh kosong."},
            "jabatan_kepala": {"required": "Jabatan kepala tidak boleh kosong."},
            "visi": {"required": "Pernyataan visi tidak boleh kosong."},
            "alamat": {"required": "Alamat tidak boleh kosong."},
            "google_maps_embed_url": {
                "required": "Embed URL peta tidak boleh kosong.",
                "invalid": "Format URL embed peta tidak valid.",
            },
            "google_maps_link": {
                "required": "Link Google Maps tidak boleh kosong.",
                "invalid": "Format link Google Maps tidak valid.",
            },
            "jam_senin_kamis": {"required": "Jam operasional Senin–Kamis tidak boleh kosong."},
            "jam_jumat": {"required": "Jam operasional Jumat tidak boleh kosong."},
            "jam_sabtu": {"required": "Jam operasional Sabtu tidak boleh kosong."},
            "jam_minggu": {"required": "Jam operasional Minggu tidak boleh kosong."},
        }

class MisiUPTDForm(forms.ModelForm):
    class Meta:
        model = MisiUPTD
        fields = ["isi"]
        widgets = {
            "isi": forms.TextInput(attrs={"class": "adm-field", "placeholder": "Tulis satu poin misi..."}),
        }
        error_messages = {
            "isi": {"required": "Isi misi tidak boleh kosong."},
        }