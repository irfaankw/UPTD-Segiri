from django import forms
from .models import Pengaduan

class PengaduanForm(forms.ModelForm):
    class Meta:
        model = Pengaduan
        fields = ["nama", "telepon", "email", "kategori", "kategori_lainnya", "pesan", "lampiran"]
        widgets = {
            "kategori": forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base_input = (
            "w-full bg-surface-container-lowest border border-outline-variant "
            "rounded-lg text-on-surface text-sm px-3.5 py-2.5 focus:outline-none "
            "focus:border-primary transition placeholder:text-outline"
        )

        self.fields["nama"].required = False
        self.fields["nama"].widget.attrs.update({
            "class": base_input,
            "placeholder": "Masukkan nama lengkap Anda (opsional)",
        })

        self.fields["telepon"].required = False
        self.fields["telepon"].widget.attrs.update({
            "class": base_input,
            "placeholder": "08xx-xxxx-xxxx",
        })

        self.fields["email"].required = False
        self.fields["email"].widget.attrs.update({
            "class": base_input,
            "placeholder": "email@contoh.com",
        })

        self.fields["kategori"].required = False  
        self.fields["kategori"].choices = Pengaduan.KATEGORI_CHOICES
        self.fields["kategori"].widget.attrs.update({"class": "peer hidden"})

        # Poin #5: field teks untuk kategori "Lainnya", disembunyikan default via JS
        self.fields["kategori_lainnya"].required = False
        self.fields["kategori_lainnya"].widget.attrs.update({
            "class": base_input,
            "placeholder": "Jelaskan kategori yang Anda maksud...",
            "id": "id_kategori_lainnya",
        })

        self.fields["pesan"].required = True
        self.fields["pesan"].widget.attrs.update({
            "class": base_input + " resize-none",
            "rows": 4,
            "placeholder": "Tuliskan masukan atau saran Anda di sini...",
        })

        self.fields["lampiran"].required = False
        self.fields["lampiran"].widget.attrs.update({
            "class": "hidden",
            "id": "id_lampiran",
        })

    def clean_nama(self):
        nama = self.cleaned_data.get("nama", "").strip()
        return nama if nama else "Anonim"

    def clean_pesan(self):
        pesan = self.cleaned_data.get("pesan", "").strip()
        if not pesan:
            raise forms.ValidationError("Pesan tidak boleh kosong.")
        return pesan

    def clean(self):
        cleaned = super().clean()
        kategori = cleaned.get("kategori")
        kategori_lainnya = cleaned.get("kategori_lainnya", "").strip()

        if not kategori:
            self.add_error("kategori", "Silakan pilih salah satu kategori.")
        elif kategori == "lainnya" and not kategori_lainnya:
            self.add_error("kategori_lainnya", "Mohon jelaskan kategori yang Anda maksud.")

        return cleaned