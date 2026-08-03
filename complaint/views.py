from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from django_ratelimit.decorators import ratelimit
from .forms import PengaduanForm

SESSION_COOLDOWN_MINUTES = 5

@require_POST
@ratelimit(key='ip', rate='3/h', method='POST', block=False)
def submit_pengaduan(request):
    # Lapis 1: rate limit per IP
    if getattr(request, 'limited', False):
        return JsonResponse({
            "success": False,
            "errors": {"pesan": [{"message": "Terlalu banyak percobaan dari alamat ini. Silakan coba lagi nanti."}]},
        }, status=429)

    # Lapis 2: cooldown per session/browser (nutup celah IP yang dipakai bareng banyak orang)
    last_submit = request.session.get('last_feedback_submit')
    if last_submit:
        elapsed = timezone.now() - timezone.datetime.fromisoformat(last_submit)
        if elapsed < timedelta(minutes=SESSION_COOLDOWN_MINUTES):
            return JsonResponse({
                "success": False,
                "errors": {"pesan": [{"message": "Mohon tunggu beberapa saat sebelum mengirim masukan lagi."}]},
            }, status=429)

    # Lapis 3: honeypot (dicek otomatis lewat form.is_valid(), karena ada di clean_website())
    form = PengaduanForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        request.session['last_feedback_submit'] = timezone.now().isoformat()
        return JsonResponse({
            "success": True,
            "message": "Masukan Anda berhasil dikirim. Terima kasih!",
        })

    return JsonResponse({
        "success": False,
        "errors": form.errors.get_json_data(),
    }, status=400)