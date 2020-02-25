# urls.py
from django.urls import path
from ventas.views import OfertaListView, OfertaEditView, OfertaDetailView, VentaListView, VentaCreateView,\
    VentaEditView, VentaDetailView, ReporteVentas, VentaEntregaView, VentaCancelarView, VentaDuplicarView,\
    VentaFindView, VentaDescuentoAdicionalView
from ventas.rviews import ProductoDetailsView, ValidarStockView


urlpatterns = [
    path('oferta', OfertaListView.as_view()),
    path('oferta/<int:pk>/', OfertaDetailView.as_view()),
    path('oferta/<int:pk>/edit', OfertaEditView.as_view()),
    path('venta', VentaListView.as_view()),
    path('venta/add', VentaCreateView.as_view()),
    path('find', VentaFindView.as_view()),
    path('venta/<int:pk>/edit', VentaEditView.as_view()),
    path('venta/<int:pk>/', VentaDetailView.as_view()),
    path('venta/<int:venta>/entrega', VentaEntregaView.as_view()),
    path('venta/<int:venta>/cancelar', VentaCancelarView.as_view()),
    path('venta/<int:venta>/duplicar', VentaDuplicarView.as_view()),
    path('detalleventa/<int:pk>/descuento', VentaDescuentoAdicionalView.as_view()),
    path('reporteventas/<int:id>', ReporteVentas, name='reporteventas'),

    path('api/productodetails/<str:producto>/<int:sucursal>', ProductoDetailsView.as_view()),
    path('api/validatestock/<int:presentacion>/<int:sucursal>/<int:cantidad>', ValidarStockView.as_view()),

]
