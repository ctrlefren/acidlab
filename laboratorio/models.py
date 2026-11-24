from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


def formula(ph):
    """CO2 (µatm) = 630 + (8 - pH) * 1000"""
    return round(630.0 + (8.0 - ph) * 1000, 2)


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

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.equipo} ({self.fecha:%d/%m/%Y})"

    def get_absolute_url(self):
        return reverse("detalle", args=[self.pk])

    @property
    def phs(self):
        return [self.ph1, self.ph2, self.ph3, self.ph4]

    @property
    def resultados(self):
        return [self.resultado1, self.resultado2, self.resultado3, self.resultado4]

    @property
    def mediciones(self):
        return [
            {"n": i + 1, "ph": p, "res": r, "critico": p < settings.PH_CRITICO}
            for i, (p, r) in enumerate(zip(self.phs, self.resultados))
        ]

    @property
    def critico(self):
        return any(p < settings.PH_CRITICO for p in self.phs)

    def calcular(self):
        for i, ph in enumerate(self.phs, start=1):
            setattr(self, f"resultado{i}", formula(ph))

    def save(self, *args, **kwargs):
        self.calcular()
        super().save(*args, **kwargs)
