from maestro.models import Producto, PresentacionxProducto, Impuesto, CatalogoxProveedor
from compras.models import DetalleCompra, OfertaCompra, Compra
from almacen.utils import update_kardex_stock
from finanzas.models import Jornada, DetalleJornada
import json


def fill_data_compra(compra, dc_form, impuestos):
    dc_form.cantidad_unidad_pedido = dc_form.cantidad_presentacion_pedido * dc_form.presentacionxproducto.cantidad
    dc_form.sub_total = dc_form.cantidad_presentacion_pedido * dc_form.precio
    ofertas_type_discount = OfertaCompra.objects.filter(detallecompra=dc_form.id, tipo__in=['2', '3'])
    descuento = 0
    for otd in ofertas_type_discount:
        if otd.tipo == '2':
            descuento += otd.retorno * (dc_form.cantidad_presentacion_pedido//otd.cantidad_compra)
        elif otd.tipo == '3':
            if dc_form.cantidad_presentacion_pedido >= otd.cantidad_compra:
                descuento += (dc_form.sub_total * otd.retorno)/100
    dc_form.descuento = descuento
    dc_form.total = dc_form.sub_total - descuento
    impuesto_array = []
    impuesto_monto = 0
    if impuestos != '':
        for i in json.loads(impuestos):
            temp_i = Impuesto.objects.get(pk=i)
            impuesto_array.append(temp_i)
            impuesto_monto += (dc_form.total * temp_i.porcentaje)/100
    dc_form.impuesto_monto = impuesto_monto
    dc_form.total_final = dc_form.total + impuesto_monto
    dc_form.is_nodeseado = False
    dc_form.save()
    if compra.tipo == '1' and compra.estado != '3':
        dc_form.cantidad_presentacion_entrega = dc_form.cantidad_presentacion_pedido
        dc_form.cantidad_unidad_entrega = dc_form.cantidad_unidad_pedido
        dc_form.is_checked = True
        dc_form.save()
        catalogo_proveedor = CatalogoxProveedor.objects.get(producto=dc_form.presentacionxproducto.producto_id,
                                                            proveedor=compra.proveedor_id)
        catalogo_proveedor.presentacionxproducto = dc_form.presentacionxproducto
        catalogo_proveedor.precio_tentativo = dc_form.precio
        catalogo_proveedor.save()
        producto = Producto.objects.get(pk=dc_form.presentacionxproducto.producto_id)
        precio_actual_compra = dc_form.total_final / dc_form.cantidad_unidad_entrega
        if producto.precio_compra < precio_actual_compra:
            producto.precio_compra = precio_actual_compra
            producto.precio_venta = producto.precio_compra + producto.utilidad_monetaria
            producto.save()
        update_kardex_stock(dc_form, '1', '1', compra)
    for im in impuesto_array:
        dc_form.impuesto.add(im)
    ofertas_type_product = OfertaCompra.objects.filter(detallecompra=dc_form.id, tipo=1)
    for ofp in ofertas_type_product:
        if dc_form.cantidad_presentacion_pedido >= ofp.cantidad_compra:
            cantidad_presentacion_pedido = ofp.retorno*(dc_form.cantidad_presentacion_pedido // ofp.cantidad_compra)
            dc_ofer = DetalleCompra(compra=compra, producto=ofp.presentacion.producto,
                                    presentacionxproducto=ofp.presentacion,
                                    cantidad_presentacion_pedido=cantidad_presentacion_pedido,
                                    cantidad_unidad_pedido=ofp.presentacion.cantidad*cantidad_presentacion_pedido,
                                    precio=0, sub_total=0, descuento=0, impuesto_monto=0, total=0, total_final=0,
                                    is_oferta=True, is_nodeseado=False)
            dc_ofer.save()
            if compra.tipo == '1' and compra.estado != '3':
                dc_ofer.cantidad_presentacion_entrega = dc_ofer.cantidad_presentacion_pedido
                dc_ofer.cantidad_unidad_entrega = dc_ofer.cantidad_unidad_pedido
                dc_ofer.is_checked = True
                dc_ofer.save()
                update_kardex_stock(dc_ofer, '1', '1', compra)


def loadtax(d):
    impuestos_model = d.impuesto.all()
    impuestos = []
    for i in impuestos_model:
        impuestos.append(str(i.id))
    d.impuesto_value = json.dumps(impuestos)
    return d


def create_ofertas(ofertas, detallecompra):
    if ofertas != '':
        oferta_array = json.loads(ofertas)
        for o in oferta_array:
            validar = validar_oferta(o)
            if validar[0]:
                oferta_orden = OfertaCompra(detallecompra=detallecompra, tipo=o[0], cantidad_compra=o[1],
                                            presentacion_compra=detallecompra.presentacionxproducto, retorno=o[2])
                if len(o) > 3:
                    oferta_orden.producto = validar[1]
                    oferta_orden.presentacion = validar[2]
                oferta_orden.save()


def recalcular_total_compra(compra):
    detallecompra = DetalleCompra.objects.filter(compra=compra.id)
    total_final = 0
    for d in detallecompra:
        total_final += d.total_final
    compra.total_final = total_final
    compra.save()


# def guardar_oferta(oferta, detalle_orden):
#     OfertaOrden.objects.filter(detalleorden=detalle_orden.id).delete()
#     ResultadoOfertaOrden.objects.filter(detalleorden=detalle_orden.id).delete()
#     if oferta != '':
#         oferta_array = json.loads(oferta)
#         for o in oferta_array:
#             validar = validar_oferta(o)
#             if validar[0]:
#                 oferta_orden = OfertaOrden(detalleorden=detalle_orden, tipo=o[0], cantidad_compra=o[1],
#                                            presentacion_compra=detalle_orden.presentacionxproducto, retorno=o[2])
#                 cantidad_oferta = int(o[1])
#                 retorno = float(o[2])
#                 resultado_orden = ResultadoOfertaOrden(detalleorden=detalle_orden)
#                 if len(o) > 3:
#                     oferta_orden.producto = validar[1]
#                     oferta_orden.presentacion = validar[2]
#                     if detalle_orden.cantidad_presentacion >= cantidad_oferta:
#                         resultado_orden.tipo = oferta_orden.tipo
#                         resultado_orden.cantidad_presentacion = (detalle_orden.cantidad_presentacion // cantidad_oferta) * retorno
#                         resultado_orden.cantidad_unidad = resultado_orden.cantidad_presentacion * validar[2].cantidad
#                         resultado_orden.producto = validar[1]
#                         resultado_orden.presentacion = validar[2]
#                         resultado_orden.save()
#                 else:
#                     if o[0] == '2':
#                         if detalle_orden.cantidad_presentacion >= cantidad_oferta:
#                             resultado_orden.tipo = oferta_orden.tipo
#                             resultado_orden.descuento = (detalle_orden.cantidad_presentacion // cantidad_oferta) * retorno
#                             resultado_orden.total = float(detalle_orden.total) - resultado_orden.descuento
#                             detalle_orden.descuento = resultado_orden.descuento
#                             detalle_orden.total_final = resultado_orden.total
#                             detalle_orden.save()
#                             resultado_orden.save()
#                     elif o[0] == '3':
#                         if detalle_orden.cantidad_presentacion >= cantidad_oferta:
#                             resultado_orden.tipo = oferta_orden.tipo
#                             resultado_orden.descuento = float(detalle_orden.total) * retorno / 100
#                             resultado_orden.total = float(detalle_orden.total) - resultado_orden.descuento
#                             detalle_orden.descuento = resultado_orden.descuento
#                             detalle_orden.total_final = resultado_orden.total
#                             detalle_orden.save()
#                             resultado_orden.save()
#                 oferta_orden.save()


# def crear_detallecompra(detalle_orden, request, compra):
#     for idx, d in enumerate(detalle_orden, start=1):
#         precio = float(request['precio-'+str(idx)])
#         detallecompra = DetalleCompra(compra=compra, producto=d.producto,
#                                       presentacionxproducto=d.presentacionxproducto,
#                                       cantidad_presentacion_entrega=d.cantidad_presentacion_pedido,
#                                       cantidad_entrega=d.cantidad_pedido, precio_sindescuento=precio)
#         oferta = request['oferta-'+str(idx)]
#         if oferta != '':
#             detallecompra.is_genoferta = True
#             oferta = json.loads(request['oferta-'+str(idx)])
#             for o in oferta:
#                 validar = validar_oferta(o)
#                 if validar[0]:
#                     aplicar_oferta(o, detallecompra, validar)
#         else:
#             detallecompra.precio = detallecompra.precio_sindescuento
#             detallecompra.descuento = 0
#             detallecompra.save()


def validar_oferta(oferta):
    is_valid = False
    retorno = []
    if oferta[0] not in ['1', '2', '3']:
        return [is_valid]
    if not int(oferta[1]) > 0:
        return [is_valid]
    if not float(oferta[2]) > 0:
        return [is_valid]
    if len(oferta) > 3:
        try:
            producto = Producto.objects.get(pk=oferta[3])
            presentacion = PresentacionxProducto.objects.get(pk=oferta[4])
        except (Producto.DoesNotExist, PresentacionxProducto.DoesNotExist) as e:
            return [is_valid]
        is_valid = True
        retorno.extend([is_valid, producto, presentacion])
        return retorno
    else:
        return [True]


# def aplicar_oferta(oferta, detallecompra, validar):
#     oferta_compra = OfertaOrden(tipo=oferta[0], cantidad_compra=oferta[1],
#                                 presentacion_compra=detallecompra.presentacionxproducto, retorno=oferta[2])
#     if len(oferta) > 3:
#         oferta_compra.producto_oferta = validar[1]
#         oferta_compra.presentacion_oferta = validar[2]
#         if detallecompra.cantidad_entrega >= int(oferta[1]):
#             producto_oferta = Producto.objects.get(pk=oferta[3])
#             presentacion_oferta = PresentacionxProducto.objects.get(pk=oferta[4])
#             cantidad_comprada = detallecompra.cantidad_entrega
#             cantidad_oferta = int(oferta[1])
#             retorno = int(oferta[2])
#             cantidad_regalo = (cantidad_comprada // cantidad_oferta) * retorno
#             detallecompra_oferta = DetalleCompra(compra=detallecompra.compra, producto=producto_oferta,
#                                                  presentacionxproducto=presentacion_oferta,
#                                                  cantidad_presentacion_entrega=cantidad_regalo,
#                                                  cantidad_entrega=cantidad_oferta * presentacion_oferta.cantidad,
#                                                  precio_sindescuento=0, descuento=0, precio=0, is_oferta=True)
#             detallecompra.precio = detallecompra.precio_sindescuento
#             detallecompra.descuento = 0
#             detallecompra.save()
#             detallecompra_oferta.save()
#             oferta_compra.detallecompra = detallecompra
#             oferta_compra.save()
#     else:
#         if oferta[0] == '2':
#             cantidad_comprada = detallecompra.cantidad_entrega
#             cantidad_oferta = int(oferta[1])
#             retorno = float(oferta[2])
#             detallecompra.descuento = (cantidad_comprada // cantidad_oferta)*retorno
#             detallecompra.precio = detallecompra.precio_sindescuento - detallecompra.descuento
#             detallecompra.save()
#             oferta_compra.detallecompra = detallecompra
#             oferta_compra.save()
#         elif oferta[0] == '3':
#             if detallecompra.cantidad_entrega >= int(oferta[1]):
#                 detallecompra.descuento = 100 * float(oferta[2])/detallecompra.precio_sindescuento
#             else:
#                 detallecompra.descuento = 0
#             detallecompra.precio = detallecompra.precio_sindescuento - detallecompra.descuento
#             detallecompra.save()
#             oferta_compra.detallecompra = detallecompra
#             oferta_compra.save()


def cargar_ofertas(detalle_compra):
    for dc in detalle_compra:
        oferta = OfertaCompra.objects.filter(detallecompra=dc.id)
        array_temp = []
        for o in oferta:
            array_temp.append(o)
        dc.promocion = array_temp
    return detalle_compra


def cargar_oferta(detalle_orden):
    oferta = OfertaCompra.objects.filter(detallecompra=detalle_orden.id)
    array_temp = []
    for o in oferta:
        if o.tipo == '1':
            array_temp.append([o.tipo, str(o.cantidad_compra), str(o.retorno), str(o.producto_id), str(o.presentacion_id)])
        else:
            array_temp.append([o.tipo, str(o.cantidad_compra), str(o.retorno)])
    detalle_orden.oferta = json.dumps(array_temp)
    return detalle_orden


# def fill_data_compra(detalle_compra, id_detalleorden):
#     detalle_orden = DetalleOrdenCompra.objects.get(pk=id_detalleorden)
#     detalle_compra.producto = detalle_orden.producto
#     detalle_compra.presentacionxproducto = detalle_orden.presentacionxproducto
#     detalle_compra.cantidad_unidad = detalle_compra.cantidad_presentacion * detalle_compra.presentacionxproducto.cantidad
#     detalle_compra.precio = detalle_compra.total / detalle_compra.cantidad_presentacion
#     detalle_compra.save()
#     # '1' y '1' significa entrada y compra para el kardex
#     update_kardex_stock(detalle_compra, '1', '1')


def recalcular_total_compra(compra):
    detallecompra = DetalleCompra.objects.filter(compra=compra.id)
    total = 0
    for d in detallecompra:
        total += d.total
    compra.total = total
    compra.save()


# def fill_data_compraoferta(detalle_compra, id_resultado_oferta):
#     resultado_oferta = ResultadoOfertaOrden.objects.get(pk=id_resultado_oferta)
#     detalle_compra.producto = resultado_oferta.producto
#     detalle_compra.presentacionxproducto = resultado_oferta.presentacionxproducto
#     detalle_compra.cantidad_unidad = detalle_compra.cantidad_presentacion * resultado_oferta.presentacionxproducto.cantidad
#     detalle_compra.precio = 0
#     detalle_compra.total = 0
#     detalle_compra = detalle_compra.save()
#     # '1' y '1' significan entrada y compra para el kardex respectivamente
#     update_kardex_stock(detalle_compra, '1', '1')


# def ordentocompra(form, user, orden):
#     detalles_orden = DetalleOrdenCompra.objects.filter(ordencompra=orden.id)
#     resultado_oferta = ResultadoOfertaOrden.objects.filter(detalleorden__ordencompra=orden.id, tipo='1')
#     estado_envio = form.cleaned_data['estado_envio']
#     tipo_comprobante = form.cleaned_data['tipo_comprobante']
#     serie_comprobante = form.cleaned_data['serie_comprobante']
#     numero_comprobante = form.cleaned_data['numero_comprobante']
#     compra = Compra(asignado=user, proveedor=orden.proveedor, almacen=orden.almacen, estado=estado_envio,
#                     orden=orden, tipo_comprobante=tipo_comprobante, serie_comprobante=serie_comprobante,
#                     numero_comprobante=numero_comprobante, total=orden.total, descuento=orden.descuento,
#                     total_final=orden.total_final)
#     if estado_envio == '1':
#         orden.estado = '2'
#     elif estado_envio == '2':
#         orden.estado = '3'
#     orden.save()
#     compra.save()
#     for do in detalles_orden:
#         detalle_compra = DetalleCompra(compra=compra, producto=do.producto,
#                                        presentacionxproducto=do.presentacionxproducto,
#                                        cantidad_presentacion_pedido=do.cantidad_presentacion,
#                                        cantidad_presentacion_entrega=do.cantidad_presentacion,
#                                        cantidad_unidad=do.cantidad_unidad, precio=do.precio, total=do.total,
#                                        descuento=do.descuento, total_final=do.total_final, is_nodeseado=False)
#         detalle_compra.save()
#         if estado_envio == '2':
#             # '1' y '1' significan entrada y compra para el kardex respectivamente
#             detalle_compra.save()
#             update_kardex_stock(detalle_compra, '1', '1', compra)
#     for ro in resultado_oferta:
#         detalle_compra = DetalleCompra(compra=compra, producto=ro.presentacion.producto,
#                                        presentacionxproducto=ro.presentacion,
#                                        cantidad_presentacion_pedido=ro.cantidad_presentacion,
#                                        cantidad_presentacion_entrega=ro.cantidad_presentacion,
#                                        cantidad_unidad=ro.cantidad_unidad, precio=0, total=0, descuento=0,
#                                        total_final=0, is_oferta=True, is_nodeseado=False)
#         detalle_compra.save()
#         if estado_envio == '2':
#             # '1' y '1' significan entrada y compra para el kardex respectivamente
#             detalle_compra.save()
#             update_kardex_stock(detalle_compra, '1', '1', compra)
#     return compra.id


def fill_data_detallecompra(detalle_compra, flag_estado, compra):
    detalle_compra.cantidad_unidad_entrega = detalle_compra.cantidad_presentacion_entrega * \
                                                detalle_compra.presentacionxproducto.cantidad
    porcentaje = 0
    if detalle_compra.is_nodeseado:
        detalle_compra.cantidad_presentacion_pedido = detalle_compra.cantidad_presentacion_entrega
        detalle_compra.cantidad_unidad_pedido = detalle_compra.cantidad_presentacion_pedido \
                                                * detalle_compra.presentacionxproducto.cantidad
        detalle_compra.is_checked = True
    else:
        impuesto = detalle_compra.impuesto.all()
        for i in impuesto:
            porcentaje += i.porcentaje
    detalle_compra.total = (detalle_compra.total_final*100)/(100+porcentaje)
    detalle_compra.impuesto_monto = detalle_compra.total_final - detalle_compra.total
    detalle_compra.sub_total = (detalle_compra.total+detalle_compra.descuento)
    detalle_compra.precio = detalle_compra.sub_total/detalle_compra.cantidad_presentacion_entrega
    detalle_compra.save()
    # '1' y '1' significa entrada y compra para el kardex
    if flag_estado == '3':
        update_kardex_stock(detalle_compra, '1', '1', compra)


def cancelarcompra(compra, asignado):
    if compra.estado != '4':
        url = ''
        try:
            jornada = Jornada.objects.get(estado=True)
        except Jornada.DoesNotExist:

            url = '/?incidencias=' + json.dumps([
                ['3', 'La caja está cerrada, no se puede cancelar.']])
            return url
        estado = compra.estado
        compra.estado = '4'
        compra.save()
        if estado == '3':
            if compra.is_pagado:
                DetalleJornada(jornada=jornada, tipo='1', target=compra.id, monto=compra.total_final,
                               descripcion='Reembolso Compra', asignado=asignado).save()
            detallecompra = DetalleCompra.objects.filter(venta=compra.id)
            for dc in detallecompra:
                update_kardex_stock(dc, '1', '3', compra)
    else:
        url = '/?incidencias=' + json.dumps([
            ['3', 'Ya se canceló']])
    return url
