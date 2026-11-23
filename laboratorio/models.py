from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


def formula(ph):
    """CO2 (µatm) = 630 + (8 - pH) * 1000"""
    return round(630 + (8 - ph) * 1000, 2)

PH_VALIDOS = [MinValueValidator(0), MaxValueValidator(14)]


class RegistroAcidificacion(models.Model):
    equipo = models.CharField("Equipo de laboratorio", max_length=100)
    fecha = models.DateTimeField("Fecha y hora", auto_now_add=True)
    ph1 = models.FloatField("Medida 1 (pH)", validators=PH_VALIDOS)
    ph2 = models.FloatField("Medida 2 (pH)", validators=PH_VALIDOS)
    ph3 = models.FloatField("Medida 3 (pH)", validators=PH_VALIDOS)
    ph4 = models.FloatField("Medida 4 (pH)", validators=PH_VALIDOS)
    resultado1 = models.FloatField(null=True, editable=False)
    resultado2 = models.FloatField(null=True, editable=False)
    resultado3 = models.FloatField(null=True, editable=False)
    resultado4 = models.FloatField(null=True, editable=False)
    leyenda = models.TextField("Leyenda de la gráfica", blank=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, editable=False,
    )

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.equipo} ({self.fecha:%d/%m/%Y})"

    def get_absolute_url(self):
        return reverse("detalle", args=[self.pk]9)

    @    