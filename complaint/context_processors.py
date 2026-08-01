from .forms import PengaduanForm

def pengaduan_form(request):
    """Menyediakan instance PengaduanForm kosong di semua template,
    supaya modal 'Sampaikan Masukan' bisa muncul di halaman manapun
    tanpa perlu tiap view mengirim form secara manual.
    """
    return {"pengaduan_form": PengaduanForm()}