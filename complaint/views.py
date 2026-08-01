from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import PengaduanForm

@require_POST
def submit_pengaduan(request):
    form = PengaduanForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        return JsonResponse({
            "success": True,
            "message": "Masukan Anda berhasil dikirim. Terima kasih!",
        })

    return JsonResponse({
        "success": False,
        "errors": form.errors.get_json_data(),
    }, status=400)