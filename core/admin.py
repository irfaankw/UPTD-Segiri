from django.contrib import admin
from .models import ProfilUPTD, MisiUPTD

class MisiInline(admin.TabularInline):
    model = MisiUPTD
    extra = 1
    max_num = 5

@admin.register(ProfilUPTD)
class ProfilUPTDAdmin(admin.ModelAdmin):
    inlines = [MisiInline]

    def has_add_permission(self, request):
        # Cegah bikin lebih dari 1 data (singleton)
        return not ProfilUPTD.objects.exists()