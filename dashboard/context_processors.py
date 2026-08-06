from complaint.models import Pengaduan

def pengaduan_pending_count(request):
    if request.user.is_authenticated:
        return {"pengaduan_pending_count": Pengaduan.objects.filter(status="baru").count()}
    return {}