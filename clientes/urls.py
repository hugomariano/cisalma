# urls.py
from django.urls import path
from clientes.views import ClienteListView, ClienteEditView, ClienteDetailView, ContactoEditView,\
    ContactoDetailView, ContactoListView

from maestro.rviews import ProductosListView


urlpatterns = [
    path('cliente/', ClienteListView.as_view()),
    path('cliente/<int:pk>/', ClienteDetailView.as_view()),
    path('cliente/<int:pk>/edit', ClienteEditView.as_view()),
    path('contacto/', ContactoListView.as_view()),
    path('contacto/<int:pk>/', ContactoDetailView.as_view()),
    path('contacto/<int:pk>/edit', ContactoEditView.as_view()),
    # API URL'S
    path('api/producto', ProductosListView.as_view()),
]
