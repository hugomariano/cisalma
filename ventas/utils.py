from maestro.models import CatalogoxProveedor, Impuesto, Sucursal
from ventas.models import OfertaVenta, DetalleVenta, Venta
from almacen.models import Stock
from almacen.utils import update_kardex_stock
from finanzas.models import Jornada, DetalleJornada
import json
from django.db.models import Max
from django.db.models import Sum


def fill_data_venta(venta, dv_form, impuestos):
    incidencia = []
    dv_form.precio = dv_form.producto.precio_venta * dv_form.presentacionxproducto.cantidad
    stock = Stock.objects.filter(almacen__sucursal=Sucursal.objects.get(pk=venta.sucursal_id))
    stock = stock.filter(producto=dv_form.presentacionxproducto.producto_id)
    stock = stock.annotate(Sum('cantidad'))
    cantidad_stock = 0
    for s in stock:
        cantidad_stock = s.cantidad__sum
        break
    cantidad_pedido = dv_form.cantidad_presentacion_pedido
    cantidad_stock_presentacion = cantidad_stock // dv_form.presentacionxproducto.cantidad
    if cantidad_pedido > cantidad_stock_presentacion:
        incidencia = ['1', dv_form.producto.descripcion,
                      dv_form.cantidad_presentacion_pedido, cantidad_stock_presentacion]
        dv_form.cantidad_presentacion_pedido = cantidad_stock_presentacion
    dv_form.cantidad_unidad_pedido = dv_form.cantidad_presentacion_pedido * dv_form.presentacionxproducto.cantidad
    dv_form.sub_total = dv_form.cantidad_presentacion_pedido * dv_form.precio
    ofertas_type_discount = OfertaVenta.objects.filter(is_active=True, producto_oferta=dv_form.producto.id,
                                                       tipo__in=['2', '3'])
    descuento = 0
    for otd in ofertas_type_discount:
        if otd.is_active:
            if otd.tipo_duracion == '1':
                if otd.stock_faltante >= dv_form.cantidad_unidad_pedido:
                    if otd.tipo == '2':
                        descuento += otd.retorno * (dv_form.cantidad_unidad_pedido//otd.cantidad_unidad_oferta)
                    elif otd.tipo == '3':
                        if dv_form.cantidad_unidad_pedido >= otd.cantidad_unidad_oferta:
                            descuento += (dv_form.sub_total * otd.retorno)/100
                else:
                    if otd.tipo == '2':
                        descuento += otd.retorno * (otd.stock_faltante//otd.cantidad_unidad_oferta)
                    elif otd.tipo == '3':
                        if dv_form.stock_faltante >= otd.cantidad_unidad_oferta:
                            descuento += (dv_form.sub_total * otd.retorno)/100
                    incidencia = ['2', dv_form.producto.descripcion,
                                  dv_form.cantidad_unidad_pedido, otd.stock_faltante]
            else:
                if otd.tipo == '2':
                    descuento += otd.retorno * (dv_form.cantidad_unidad_pedido // otd.cantidad_unidad_oferta)
                elif otd.tipo == '3':
                    if dv_form.cantidad_unidad_pedido >= otd.cantidad_unidad_oferta:
                        descuento += (dv_form.sub_total * otd.retorno) / 100
    dv_form.descuento = descuento
    dv_form.total = dv_form.sub_total - descuento
    impuesto_array = []
    impuesto_monto = 0
    if impuestos != '' and impuestos != '[]':
        for i in json.loads(impuestos):
            temp_i = Impuesto.objects.get(pk=i)
            impuesto_array.append(temp_i)
            impuesto_monto += (dv_form.total * temp_i.porcentaje)/100
    dv_form.impuesto_monto = impuesto_monto
    dv_form.total_final = dv_form.total + impuesto_monto
    dv_form.save()
    if venta.tipo == '1' and venta.estado != '3':
        dv_form.cantidad_presentacion_entrega = dv_form.cantidad_presentacion_pedido
        dv_form.cantidad_unidad_entrega = dv_form.cantidad_unidad_pedido
        dv_form.save()
        update_kardex_stock(dv_form, '2', '2', venta)
    for im in impuesto_array:
        dv_form.impuesto.add(im)
    ofertas_type_product = OfertaVenta.objects.filter(producto_oferta=dv_form.producto.id, tipo=1)
    for ofp in ofertas_type_product:
        if ofp.is_active:
            if ofp.tipo_duracion == '1':
                if ofp.stock_faltante >= dv_form.cantidad_unidad_pedido:
                    if dv_form.cantidad_unidad_pedido >= ofp.cantidad_unidad_oferta:
                        dv_oferta = DetalleVenta(venta=venta, producto=ofp.producto_retorno,
                                                 presentacionxproducto=ofp.presentacion_retorno,
                                                 cantidad_presentacion_pedido=ofp.retorno,
                                                 cantidad_unidad_pedido=
                                                 ofp.retorno*(dv_form.cantidad_unidad_pedido//ofp.cantidad_unidad_oferta),
                                                 precio=0, sub_total=0, descuento=0, impuesto_monto=0, total=0,
                                                 total_final=0, is_oferta=True)
                        dv_oferta.save()
                else:
                    dv_oferta = DetalleVenta(venta=venta, producto=ofp.producto_retorno,
                                             presentacionxproducto=ofp.presentacion_retorno,
                                             cantidad_presentacion_pedido=ofp.retorno,
                                             cantidad_unidad_pedido=
                                             ofp.retorno*(ofp.stock_faltante//ofp.cantidad_unidad_oferta),
                                             precio=0,
                                             sub_total=0, descuento=0, impuesto_monto=0, total=0, total_final=0,
                                             is_oferta=True)
                    dv_oferta.save()
                    incidencia = ['2', dv_form.producto.descripcion,
                                  dv_form.cantidad_unidad_pedido, ofp.stock_faltante]
            else:
                dv_oferta = DetalleVenta(venta=venta, producto=ofp.producto_retorno,
                                         presentacionxproducto=ofp.presentacion_retorno,
                                         cantidad_presentacion_pedido=ofp.retorno,
                                         cantidad_unidad_pedido=
                                         ofp.retorno * (dv_form.cantidad_unidad_pedido // ofp.cantidad_unidad_oferta),
                                         precio=0, sub_total=0, descuento=0, impuesto_monto=0, total=0,
                                         total_final=0, is_oferta=True)
                dv_oferta.save()
    return incidencia


def load_tax(d):
    impuestos_model = d.impuesto.all()
    impuestos = []
    for i in impuestos_model:
        impuestos.append(str(i.id))
    d.impuesto_value = json.dumps(impuestos)
    return d


def create_venta_txt(venta_id):
    venta = Venta.objects.get(id=venta_id)
    detalleventa = DetalleVenta.objects.filter(venta=venta_id)
    f = open("static/dinamicallygenerated/txt/venta-" + str(venta_id) + ".txt", "w+")
    f.write("       ABADS E.I.R.L." + "\n")
    f.write("\n")
    f.write("JR. SAN MARTIN 871" + "\n")
    f.write("HUANUCO - HUANUCO - HUANUCO" + "\n")
    f.write("RUC: 20528995676" + "\n")
    f.write("*****************************" + "\n")
    f.write("       TICKET NRO: " + str(venta_id) + "\n")
    f.write("*****************************" + "\n")
    f.write("VENTA: " + str(venta_id) + "\n")
    if venta.cliente is None:
        f.write("CLIENTE: REGULAR \n")
    else:
        f.write("CLIENTE: " + str(venta.cliente) + "\n")
    f.write("FORM.PAGO: " + venta.get_tipo_pago_display() + "\n")
    fecha = str(venta.fechahora_creacion)
    new_fecha = fecha[:19]
    f.write("FECHA:" + new_fecha + "\n")
    f.write("*****************************" + "\n")
    f.write("Prod/Pres Cant  Precio  Total" + "\n")
    f.write("*****************************" + "\n")
    sub_total = 0

    for dv in detalleventa:
        f.write(
            dv.presentacionxproducto.producto.descripcion + "//" +
            dv.presentacionxproducto.presentacion.descripcion + "\n")
        f.write("    " + str(dv.cantidad_presentacion_pedido)
                + '(' + str(dv.cantidad_unidad_pedido) + ')'
                + "  S/." + str(dv.precio) + " S/. " + str(
            dv.total_final) + "\n")
        f.write("\n")
        sub_total = sub_total + dv.total_final

    f.write("*****************************" + "\n")
    f.write("SUB TOTAL      S/ :" + ' ' + str(venta.sub_total) + "\n")
    f.write("DESCUENTO      S/ :" + ' ' + str(venta.descuento) + "\n")
    f.write("IMP. MONTO     S/ :" + ' ' + str(venta.impuesto_monto) + "\n")
    f.write("TOTAL          S/ :" + ' ' + str(venta.total_final) + "\n")
    f.write("*****************************" + "\n")
    f.write("     GRACIAS POR SU COMPRA." + "\n")
    f.write("*****************************" + "\n")
    f.write("*****************************" + "\n")
    f.close()


def fill_data_detalleventa(detalle_venta, flag_estado, venta):
    detalle_venta.cantidad_unidad_entrega = detalle_venta.cantidad_presentacion_entrega * \
                                            detalle_venta.presentacionxproducto.cantidad
    porcentaje = 0
    impuesto = detalle_venta.impuesto.all()
    for i in impuesto:
        porcentaje += i.porcentaje
    detalle_venta.sub_total = (detalle_venta.cantidad_presentacion_entrega*detalle_venta.precio)
    detalle_venta.total = (detalle_venta.total_final*100)/(100+porcentaje)
    detalle_venta.impuesto_monto = detalle_venta.total_final - detalle_venta.total
    detalle_venta.precio = detalle_venta.sub_total/detalle_venta.cantidad_presentacion_entrega
    detalle_venta.save()
    # '2' y '2' significa salida y venta para el kardex
    if flag_estado == '3':
        update_kardex_stock(detalle_venta, '2', '2', venta)


def cancelarventa(venta, asignado):
    if venta.estado != '4':
        url = ''
        try:
            jornada = Jornada.objects.get(estado=True)
        except Jornada.DoesNotExist:
            url = '/?incidencias=' + json.dumps([
                ['3', 'La caja está cerrada, no se puede cancelar.']])
            return url
        estado = venta.estado
        venta.estado = '4'
        venta.save()
        if estado == '3':
            if venta.is_pagado:
                DetalleJornada(jornada=jornada, tipo='2', target=venta.id, monto=venta.total_final,
                               descripcion='Reembolso Venta', asignado=asignado).save()
            detalleventa = DetalleVenta.objects.filter(venta=venta.id)
            for dv in detalleventa:
                update_kardex_stock(dv, '1', '4', venta)
    else:
        url = '/?incidencias=' + json.dumps([
            ['3', 'Ya se canceló']])
    return url
