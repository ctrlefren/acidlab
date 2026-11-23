from django.contrib import admin
from .models import RegistroAcidificacion


@admin.register(RegistroAcidificacion)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ("equipo", "fecha", "ph1", "ph2", "ph3", "ph4")
    search_fields = ("equipo",)
    readonly_fields = ("resultado1", "resultado2", "resultado3", "resultado4")