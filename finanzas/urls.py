# urls.py
from django.urls import path
from finanzas.views import JornadaListView, JornadaDetailView, DetalleJornadaCreateView, JornadaCloseView,\
    JornadaCreateView, CuentaClienteListView, CuentaClienteDetailView, PagoClienteCreateView, CuentaProveedorListView,\
    CuentaProveedorDetailView, PagoProveedorCreateView, VentaPagoView, CompraPagoView


urlpatterns = [
    path('jornada', JornadaListView.as_view()),
    path('jornada/<int:pk>/', JornadaDetailView.as_view()),
    path('detallejornada/add/<int:jornada>/', DetalleJornadaCreateView.as_view()),
    path('jornada/close/<int:jornada>/', JornadaCloseView.as_view()),
    path('pagoventa/<int:venta>/', VentaPagoView.as_view()),
    path('pagocompra/<int:compra>/', CompraPagoView.as_view()),
    path('jornada/open/', JornadaCreateView.as_view()),
    path('cuentacliente', CuentaClienteListView.as_view()),
    path('cuentacliente/<int:pk>/', CuentaClienteDetailView.as_view()),
    path('pagocliente/add/<int:cuentacliente>/', PagoClienteCreateView.as_view()),
    path('cuentaproveedor', CuentaProveedorListView.as_view()),
    path('cuentaproveedor/<int:pk>/', CuentaProveedorDetailView.as_view()),
    path('pagoproveedor/add/<int:cuentaproveedor>/', PagoProveedorCreateView.as_view()),
]
