from django.urls import path
from . import views

urlpatterns = [
    path("", views.RegistroListView.as_view(), name="lista"),
    path("registro/nuevo/", views.RegistroCreateView.as_view(), name="crear"),
    path("registro/<int:pk>/", views.RegistroDetailView.as_view(), name="detalle"),
    path("registro/<int:pk>/editar/", views.RegistroUpdateView.as_view(), name="editar"),
    path("registro/<int:pk>/eliminar/", views.RegistroDeleteView.as_view(), name="eliminar"),
]