from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from .forms import RegistroForm
from .models import RegistroAcidificacion


def alerta_critica(request, registro):
    if registro.critico:
        messages.error(
            request,
            f"¡Acidez crítica! Hay al menos una medida con pH menor a {settings.PH_CRITICO}.",
        )


class RegistroListView(ListView):
    model = RegistroAcidificacion
    template_name = "laboratorio/registro_list.html"
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            cond = Q(equipo__icontains=q)
            fecha = parse_date(q)
            if fecha:
                cond |= Q(fecha__date=fecha)
            qs = qs.filter(cond)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        return ctx


class RegistroDetailView(DetailView):
    model = RegistroAcidificacion
    template_name = "laboratorio/registro_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        r = self.object
        ctx["chart"] = {
            "labels": [f"Medida {i}" for i in range(1, 5)],
            "ph": r.phs,
            "co2": r.resultados,
        }
        return ctx


class RegistroCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = RegistroAcidificacion
    form_class = RegistroForm
    template_name = "laboratorio/registro_form.html"
    success_message = "Medición registrada y calculada correctamente."

    def form_valid(self, form):
        resp = super().form_valid(form)
        alerta_critica(self.request, self.object)
        return resp


class RegistroUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = RegistroAcidificacion
    form_class = RegistroForm
    template_name = "laboratorio/registro_form.html"
    success_message = "Medición actualizada y recalculada."

    def form_valid(self, form):
        resp = super().form_valid(form)
        alerta_critica(self.request, self.object)
        return resp


class RegistroDeleteView(LoginRequiredMixin, DeleteView):
    model = RegistroAcidificacion
    template_name = "laboratorio/registro_confirm_delete.html"
    success_url = reverse_lazy("lista")

    def form_valid(self, form):
        messages.success(self.request, "Registro eliminado.")
        return super().form_valid(form)