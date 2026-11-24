from django import forms
from .models import RegistroAcidificacion


class RegistroForm(forms.ModelForm):
    class Meta:
        model = RegistroAcidificacion
        fields = ["equipo", "ph1", "ph2", "ph3", "ph4", "leyenda"]
        widgets = {"leyenda": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["leyenda"].required = True
        for name, campo in self.fields.items():
            campo.widget.attrs["class"] = "form-control"
            if name.startswith("ph"):
                campo.widget.attrs.update({"step": "0.01", "min": 0, "max": 14})