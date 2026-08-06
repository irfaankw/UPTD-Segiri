from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

def staff_required(view_func):
    """Wajib login DAN wajib is_staff=True. Kalau login tapi bukan staff, langsung logout paksa."""
    @wraps(view_func)
    @login_required(login_url='dashboard:login')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            logout(request)
            messages.error(request, "Akun kamu tidak memiliki akses ke dashboard.")
            return redirect('dashboard:login')
        return view_func(request, *args, **kwargs)
    return wrapper