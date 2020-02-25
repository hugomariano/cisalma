var sucursal_id = document.getElementById('sucursal_id').value;
var impuesto_select = document.getElementById('id_impuesto');
var detalleventa_to_save = document.getElementById('detalleventa_to_save');
var detalleventa_to_delete = document.getElementById('detalleventa_to_delete');
var current_pos = document.getElementById("current_pos");
var addbutton = document.getElementById("add_btn");
var tr_empty = document.getElementById("tr_detalleventa_empty");
var tbody_detalleorden = document.getElementById("tbody_detalleventa");
var btn_save_impuesto = document.getElementById('save_impuesto');
var div_promocion_empty = document.getElementById('div_promocion_empty');
var body_promociones = document.getElementById('body_promociones');
var div_producto_empty = document.getElementById('div_producto_empty');
var btn_promocion = document.querySelectorAll('.promocion');
var current_pos_promocion = document.getElementById('current_pos_promocion');
var current_pos_impuesto = document.getElementById('current_pos_impuesto');

function init_ventaedit() {
    var pos = [];
    var prod = [];
    var data = [];
    for (var i = 1; i <= parseInt(current_pos.value); i++) {
        var tr = document.getElementById('tr_dv_'+i);
        var prod_select = tr.querySelector('.producto');
        var prod_value = prod_select.value;
        prod_select.removeAttribute('id');
        prod_select.setAttribute('data-pos', i);
        pos.push(i);
        prod.push(prod_value);
    }
    var list_pos = pos.join(',');
    var list_prod = prod.join(',');
    detalleventa_to_save.value=list_pos;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           data = JSON.parse(xhttp.responseText);
        }
    };
    xhttp.open("GET", "/ventas/api/productodetails/" + list_prod + "/" + sucursal_id, false);
    xhttp.send();
    init_save_impuesto_button();
    init_load_basicdata(data);
    init_cant_blur();
    trigger_blur_cantidad();
    init_prod_change();
    init_pres_change();
    init_add_button();
    init_tax_button();
    init_delete_button();
    init_keypress();
    init_promocion_button();
}
function init_load_basicdata(data) {
    if(typeof data['presentacion'] !== 'undefined') {
        for (var i = 0; i < data['presentacion'].length; i++) {
            var opt = document.createElement('option');
            opt.value = data['presentacion'][i]['id'];
            opt.innerHTML = data['presentacion'][i]['presentacion']['descripcion'];
            opt.setAttribute("data-cantidad", data['presentacion'][i]['cantidad']);
            var select = document.getElementById('sel_pre_' + data['presentacion'][i]['producto']);
            select.append(opt)
        }
    }
    var selects = document.getElementsByClassName('presentacionxproducto');
    for (var i = 1; i < selects.length; i++){
        var selected = selects[i].getAttribute("data-selected");
        selects[i].value=selected;
        $(selects[i]).select2();
    }
    $(".select2-container--default").removeAttr('style').css("width","100%");
    if(typeof data['oferta'] !== 'undefined') {
        var tempdata = [];
        for (var i = 0; i < data['oferta'].length; i++) {
            if(typeof tempdata[data['oferta'][i]['producto_oferta']['id']] === 'undefined'){
                tempdata[data['oferta'][i]['producto_oferta']['id']] = [];
            }
            tempdata[data['oferta'][i]['producto_oferta']['id']].push(data['oferta'][i])
        }
        for (var i = 0; i < tempdata.length; i++) {
            if(typeof tempdata[i] !== 'undefined') {
                var tr = document.querySelector('tr[data-prod="'+i+'"]');
                tr.querySelector('.promocion_inp').value = convertOfertatoString(tempdata[i]);
                tr.querySelector('.promocion').classList.remove("btn-default");
                tr.querySelector('.promocion').classList.add("btn-info");
            }
        }
    }
    if(typeof data['precio'] !== 'undefined') {
        var tempdata = [];
        for (var i = 0; i < data['precio'].length; i++) {
            var tr = document.querySelector('tr[data-prod="'+data['precio'][i]['id']+'"]');
            var select = tr.querySelector('.presentacionxproducto');
            tr.querySelector('.precio_inp').value = (data['precio'][i]['precio_venta']).toFixed(2);
            tr.querySelector('.td_precio').innerHTML = (data['precio'][i]['precio_venta'] * select.options[select.selectedIndex].getAttribute("data-cantidad")).toFixed(2);
            var impuestos = tr.querySelector('.impuesto_inp').value;
            if (impuestos !== '' && impuestos !== '[]') {
                current_pos_impuesto.value = tr.querySelector('.tax').getAttribute("data-pos");
                impuestos = JSON.parse(impuestos);
                $(impuesto_select).val(impuestos).change();
                var event = new Event('click');
                btn_save_impuesto.dispatchEvent(event);
            }
        }
    }
}
function trigger_blur_cantidad() {
    var cantidad = document.querySelectorAll('.cantidadpresentacion')
    for (var i = 1; i < cantidad.length; i++) {
        var event = new Event('blur');
        cantidad[i].dispatchEvent(event);
    }
}


function init_prod_change() {
    $('.producto').on("select2:selecting", function(e) {
       prod_change(this, e.params.args.data.id,e);
    });
}
function init_pres_change() {
    $('.presentacionxproducto').on("select2:selecting", function(e) {
       action_pres_change(this, e.params.args.data.id, e.params);
    });
}

function init_cant_blur() {
    var cant = document.querySelectorAll('.cantidadpresentacion');
    for (var i = 0; i < cant.length; i++) {
        cant[i].addEventListener("blur", action_cant_blur);
    }
}
function init_tax_button() {
    var tax = document.querySelectorAll('.tax');
    for (var i = 0; i < tax.length; i++) {
        tax[i].addEventListener("click", action_tax_button);
    }
}

function action_tax_button() {
    var tr = this.parentElement.parentElement;
    var pos = this.getAttribute('data-pos');
    var current_pos = current_pos_impuesto.value;
    var impuesto_inp = tr.querySelector('.impuesto_inp').value;
    if(impuesto_inp !== ''){
        impuesto_inp = JSON.parse(impuesto_inp);
    }else{
        impuesto_inp = [];
    }
    if(pos !== current_pos){
        $(impuesto_select).val(impuesto_inp).change();
    }
    $('#modal-impuesto').modal('show');

    current_pos_impuesto.value = pos;
}

function action_cant_blur() {
    var tr = this.parentElement.parentElement;
    var xhttp = new XMLHttpRequest();
    var cantidad_dom = this;
    var data = [];
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(xhttp.responseText);
            if(data['status']===0){
                cantidad_dom.value = data['maximo'];
                alert('Stock insuficiente la cantidad máxima disponible es:'+data['maximo']);
            }
            action_calcular_line_total(tr, '');
            action_calcular_total();
        }
    };
    var presentacion_id = tr.querySelector('.presentacionxproducto').value;
    var cantidad = this.value;
    xhttp.open("GET", "/ventas/api/validatestock/" + presentacion_id + "/" + sucursal_id + "/" + cantidad, false);
    xhttp.send();
}


function action_calcular_line_total(tr, value) {
    var cantidad = tr.querySelector('.cantidadpresentacion').value;
    var precio = tr.querySelector('.td_precio').innerHTML;
    var impuesto = tr.querySelector('.impuesto_inp').value;
    if(tr.querySelector('.promocion_inp').value !== ''){
        var oferta = JSON.parse(tr.querySelector('.promocion_inp').value);
    }else{
        var oferta = [];
    }
    var descuento = 0;
    var td_descuento = tr.querySelector('.td_descuento');
    var current_cantidad_presentacion;
    var presentacionxproducto = tr.querySelector('.presentacionxproducto');
    var opt = '';
    if(value === ''){
        opt = presentacionxproducto.options[presentacionxproducto.selectedIndex];
        current_cantidad_presentacion = parseFloat(opt.getAttribute('data-cantidad'));
    }else{
        current_cantidad_presentacion = value;
    }

    if(cantidad !== '' && precio !== ''){
        var subtotal = parseFloat(precio)*parseFloat(cantidad);
        for (var i = 0; i < oferta.length; i++) {
            var temp_ofer = JSON.parse(oferta[i]);
            if (temp_ofer['tipo'] === '2' || temp_ofer['tipo'] === '3'){
                var ofer_cantidad = parseFloat(temp_ofer['cantidad_oferta']);
                var ofer_cantidad_presentacion = parseFloat(temp_ofer['presentacion_oferta']['cantidad']);
                var ofer_retorno = parseFloat(temp_ofer['retorno']);
                var ofer_cantidad_unitaria = ofer_cantidad * ofer_cantidad_presentacion;
                var current_cantidad = parseFloat(cantidad);
                var current_cantidad_unitaria = current_cantidad * current_cantidad_presentacion;
                if (temp_ofer['tipo'] === '2'){
                    descuento += (Math.floor(current_cantidad_unitaria/ofer_cantidad_unitaria)*ofer_retorno)
                }else if(temp_ofer['tipo'] === '3' && current_cantidad_unitaria>=ofer_cantidad_unitaria){
                    descuento += ((subtotal*ofer_retorno)/100)
                }
             }
        }
        tr.querySelector('.td_subtotal').innerHTML = subtotal.toFixed(2);
        td_descuento.innerHTML = descuento;
        var impuesto_value = 0 ;
        if(impuesto !== '' && impuesto !== '[]'){
            impuesto = JSON.parse(impuesto);
            impuesto_value = get_impuesto_value(impuesto, subtotal - parseFloat(descuento));
        }
        tr.querySelector('.td_total').innerHTML = (subtotal - parseFloat(descuento) + impuesto_value).toFixed(2);
    }else{
        tr.querySelector('.td_subtotal').innerHTML = 0;
        td_descuento.innerHTML = 0;
        tr.querySelector('.td_total').innerHTML = 0;
    }
}
function prod_change(obj, new_value,e) {
    var id_prod = new_value;
    if(!validar_duplicado_prod(id_prod)) {
        var current_tr = document.getElementById('tr_dv_' + obj.getAttribute('data-pos'));
        var presentacion_select = current_tr.querySelector('.presentacionxproducto');
        var options_length = presentacion_select.options.length;
        var data = [];
        for (var i = 0; i < options_length; i++) {
            presentacion_select.options[0].remove();
        }
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                data = JSON.parse(xhttp.responseText);
            }
        };
        xhttp.open("GET", "/ventas/api/productodetails/" + id_prod + "/" + sucursal_id, false);
        xhttp.send();
        var datapresentacion = data['presentacion'];
        for (var i = 0; i < datapresentacion.length; i++) {
            var opt = document.createElement('option');
            opt.value = datapresentacion[i]['id'];
            opt.innerHTML = datapresentacion[i]['presentacion']['descripcion'];
            opt.setAttribute("data-cantidad", datapresentacion[i]['cantidad']);
            presentacion_select.append(opt);
        }
        presentacion_select.value = '';
        $(presentacion_select).select2('open');
        var dataprecio = data['precio'];
        current_tr.querySelector('.precio_inp').value = parseFloat(dataprecio[0]['precio_venta']).toFixed(2);
        current_tr.querySelector('.td_precio').innerHTML = parseFloat(dataprecio[0]['precio_venta']).toFixed(2);
        var dataoferta = data['oferta'];
        if (dataoferta.length > 0){
            current_tr.querySelector('.promocion_inp').value = convertOfertatoString(dataoferta);
            current_tr.querySelector('.promocion').classList.remove("btn-default");
            current_tr.querySelector('.promocion').classList.add("btn-info");
        }
    }else{
        alert('No se puede duplicar productos.');
        e.preventDefault();
    }
}

function convertOfertatoString(dataoferta) {
    var datareturn = [];
    for (var i = 0; i < dataoferta.length; i++) {
            datareturn.push(JSON.stringify(dataoferta[i]));
    }
    return JSON.stringify(datareturn)
}

function validar_duplicado_prod(id_prod) {
    var select_prod = document.querySelectorAll('.producto');
    var resp = false;
    for (var i = 0; i < select_prod.length; i++) {
        if (id_prod == select_prod[i].value){
            if(!select_prod[i].classList.contains('promocion')){
                resp = true;
                break;
            }
        }
    }
    return resp
}
function action_pres_change(obj, new_value) {
    var tr = obj.parentElement.parentElement;
    var cantidadpresentacion = obj.querySelector('option[value="'+new_value+'"]').getAttribute('data-cantidad');
    var precio = parseFloat(tr.querySelector('.precio_inp').value);
    tr.querySelector('.td_precio').innerHTML = (precio * parseFloat(cantidadpresentacion)).toFixed(2);
    action_calcular_line_total(tr, cantidadpresentacion);
    var cantidad_dom = tr.querySelector('.cantidadpresentacion');
    setTimeout(function(){$(cantidad_dom).focus();},0);
}

function init_add_button() {
    addbutton.addEventListener("click", function () {
        var temp_tr = tr_empty.cloneNode(true);
        temp_tr.removeAttribute("id");
        var select = temp_tr.querySelector(".producto");
        var select_presentacion = temp_tr.querySelector(".presentacionxproducto");
        var cantidad_presentacion = temp_tr.querySelector(".cantidadpresentacion");
        var tax = temp_tr.querySelector('.tax');
        cantidad_presentacion.addEventListener('keypress', function (e) {
            if(e.keyCode == 13){
                setTimeout(function(){$(precio).focus();},0);
                e.preventDefault();
            }
        });
        tax.addEventListener("click", action_tax_button);
        var impuesto_inp = temp_tr.querySelector('.impuesto_inp');
        var pos = (parseInt(current_pos.value) + 1).toString();
        impuesto_inp.setAttribute('name', 'dv'+pos+'-impuesto_inp');
        var promocion = temp_tr.querySelector(".promocion");
        var promocion_inp = temp_tr.querySelector(".promocion_inp");
        promocion_inp.setAttribute('name', 'oferta-'+pos);
        promocion.setAttribute('data-pos', pos);
        tax.setAttribute('data-pos', pos);
        promocion.addEventListener('click', action_btn_promocion);
        select.removeAttribute('name');
        select.setAttribute('name', 'dv'+pos+'-producto');
        select.setAttribute('data-pos', pos);
        select.setAttribute('required', 'required');
        cantidad_presentacion.setAttribute('required', 'required');
        cantidad_presentacion.addEventListener("blur", action_cant_blur);
        cantidad_presentacion.removeAttribute('name');
        cantidad_presentacion.setAttribute('name', 'dv'+pos+'-cantidad_presentacion_pedido');
        cantidad_presentacion.addEventListener('keypress', function (e) {
            if(e.keyCode == 13){
                cantidad_presentacion.blur();
                e.preventDefault();
            }
        });
        select_presentacion.classList.add('sel_presentacionxproducto');
        select_presentacion.setAttribute('required', 'required');
        select_presentacion.removeAttribute('name');
        select_presentacion.setAttribute('name', 'dv'+pos+'-presentacionxproducto');
        $(select_presentacion).select2({placeholder: "Seleccione el Producto", minimumResultsForSearch: -1});
        $(select_presentacion).on("select2:selecting", function(e) {
            action_pres_change(this, e.params.args.data.id);
        });
        $(select).select2({placeholder: "Seleccione un Producto"});
        $(select).on("select2:selecting", function(e) {
            prod_change(this, e.params.args.data.id, e);
        });
        var delete_button = temp_tr.querySelector('.delete_hdn');
        current_pos.value = pos;
        delete_button.addEventListener('click', action_delete);
        temp_tr.setAttribute("id", "tr_dv_"+pos);
        tbody_detalleorden.appendChild(temp_tr);
        $(".select2-container--default").removeAttr('style').css("width","100%");
        if(detalleventa_to_save.value === ""){
            detalleventa_to_save.value = pos;
        }else{
            var to_save = detalleventa_to_save.value.split(',');
            to_save.push(pos);
            detalleventa_to_save.value = to_save.join(',');
        }
        $(select).select2('open');
    });
}
function init_delete_button() {
    var delete_btns = document.getElementsByClassName('delete');
    for (var i = 0; i < delete_btns.length; i++) {
        delete_btns[i].addEventListener('click', action_delete);
    }
}

function action_delete() {
   var tr_content = this.parentElement.parentElement;
   var tr_id = tr_content.getAttribute('id');
   var pos = tr_id.split('_')[2];
   var data_id = tr_content.getAttribute('data-id');
   var current_delete = detalleventa_to_delete.value;
   var current_save = detalleventa_to_save.value;
   var array_save = current_save.split(',');
   if(data_id != null){
        if(current_delete === ''){
            detalleventa_to_delete.value = data_id;
        }else{
            var array_delete = current_delete.split(',');
            array_delete.push(data_id);
            detalleventa_to_delete.value = array_delete.join(',');
        }
   }
    for (var i = 0; i < array_save.length; i++) {
        if(array_save[i] === pos) {
            array_save.splice(i, 1);
        }
    }
    detalleventa_to_save.value = array_save.join(',');
    document.getElementById('tr_dv_'+pos).remove();
}


function action_calcular_total() {
    var td_total = document.querySelectorAll('.td_total');
    var total = 0;
    for(var i = 0; i < td_total.length; i++){
        total += parseFloat(td_total[i].innerHTML);
    }
    document.getElementById('orden_total').innerHTML = total;
}
function init_keypress() {
    document.addEventListener('keypress', function (e) {
        if(e.keyCode == 33){
            var event = new Event('click');
            addbutton.dispatchEvent(event);
        }
    });
    var cant = document.querySelectorAll('.cantidadpresentacion');
    for (var i = 0; i < cant.length; i++) {
        cant[i].addEventListener('keypress', function (e) {
            if(e.keyCode == 13){
                var tr = this.parentElement.parentElement;
                var precio = tr.querySelector('.precio');
                setTimeout(function(){$(precio).focus();},0);
                e.preventDefault();
            }
        });
    }
}

function get_decimal_separator() {
    var n = 1.1;
    n = n.toLocaleString().substring(1, 2);
    return n;
}


function init_promocion_button() {
    for (var i =0; i < btn_promocion.length; i++){
        btn_promocion[i].addEventListener('click', action_btn_promocion);
    }
}




function action_btn_promocion() {
    var pos = this.getAttribute('data-pos');
    var current_pos = current_pos_promocion.value;
    var current_tr  = document.getElementById('tr_dv_'+pos);
    var promocion_inp = current_tr.querySelector('.promocion_inp');
    if(pos != current_pos){
        body_promociones.innerHTML = '';
        if(promocion_inp.value !== ''){
            var data = JSON.parse(promocion_inp.value);
        }else{
             var data = [];
        }
        for (var i =0; i < data.length; i++){
            var temp_data = JSON.parse(data[i]);
            switch (temp_data['tipo']) {
                case "1":
                    var dt = document.createElement("dt");
                    dt.setAttribute("class", "inverse");
                    dt.innerHTML = 'Regalo de Productos.';
                    var dd = document.createElement("dd");
                    dd.innerHTML = 'Por cada '+ temp_data['cantidad_oferta'] +' '+
                        temp_data['presentacion_oferta']['presentacion']['descripcion'] +
                        ' llevate: '+ temp_data['retorno'] + ' ' + temp_data['producto_retorno']['descripcion']
                        + ' en ' + temp_data['presentacion_retorno']['presentacion']['descripcion'];
                    break;
                case "2":
                    var dt = document.createElement("dt");
                    dt.setAttribute("class", "inverse");
                    dt.innerHTML = 'Descuento en Efectivo.';
                    var dd = document.createElement("dd");
                    dd.innerHTML = 'Por cada ' + temp_data['cantidad_oferta'] +' '+temp_data['presentacion_oferta']['presentacion']['descripcion']  +' recibes un descuento de : S/.'+
                        temp_data['retorno'];
                    break;
                case "3":
                    var dt = document.createElement("dt");
                    dt.setAttribute("class", "inverse");
                    dt.innerHTML = 'Descuento por Porcentaje.';
                    var dd = document.createElement("dd");
                    dd.innerHTML = 'Si compras al menos ' + temp_data['cantidad_oferta'] + ' recibes un descuento del '+
                        temp_data['retorno']+'%';
                    break;
            }
            body_promociones.appendChild(dt);
            body_promociones.appendChild(dd);
        }
    }
    $('#modal-promocion').modal('show');
    current_pos_promocion.value = pos;

}

function init_save_impuesto_button() {
    btn_save_impuesto.addEventListener('click', function () {
        var current_pos = current_pos_impuesto.value;
        var current_tr  = document.getElementById('tr_dv_'+current_pos);
        var td_impuesto = current_tr.querySelector('.td_impuesto');
        var impuesto_inp = current_tr.querySelector('.impuesto_inp');
        td_impuesto.innerHTML = '';
        var temp_value = [];
         for (var i = 0; i < impuesto_select.options.length; i++) {
              if(impuesto_select.options[i].selected){
                  temp_value.push(impuesto_select.options[i].value);
              }
      }
        impuesto_inp.value = JSON.stringify(temp_value);
        var current_values = GetSelectValues(impuesto_select);
        for (var i=0 ; i< current_values.length; i++) {
            var temp_a = document.createElement("a");
            temp_a.setAttribute('href', '#');
            temp_a.addEventListener("click", action_tax_button);
            var temp_br = document.createElement("br");
            temp_a.text = current_values[i][1];
            temp_a.setAttribute('data-pos',current_pos);
            td_impuesto.appendChild(temp_a);
            td_impuesto.appendChild(temp_br);
          }
        action_calcular_line_total(current_tr, '');
        $('#modal-impuesto').modal('hide');
    });
}
function get_impuesto_value(impuesto, subtotal){
    var impuesto_value = 0;
    for (var i = 0; i < impuesto_select.options.length; i++) {
        for(var j = 0; j < impuesto.length; j++){
            if(impuesto_select.options[i].value === impuesto[j] ){
              var opt_text = impuesto_select.options[i].text;
              opt_text = opt_text.split("- ")[1];
                opt_text = opt_text.substr(0, opt_text.length -1);
                impuesto_value = ((subtotal* parseFloat(opt_text))/100)
            }
        }
      }
    return impuesto_value;
}

function GetSelectValues(select) {
  var result = [];
  var options = select && select.options;
  var opt;

  for (var i=0, iLen=options.length; i<iLen; i++) {
    opt = options[i];

    if (opt.selected) {
      result.push([opt.value, opt.text]);
    }
  }
  return result;
}

function action_change_tipoprom(obj, new_id) {
    var div_row = obj.parentElement.parentElement;
    var div_dinamic = div_row.querySelectorAll('.div_prom_dinamico');
    for (var i =0; i < div_dinamic.length; i++){
        div_dinamic[i].remove();
    }
    if(new_id == 1){
        div_row.insertAdjacentHTML('beforeend', prom_control1);
        var temp_selprod = div_producto_empty.querySelector('.producto').cloneNode(true);
        temp_selprod.classList.add("promocion");
        div_row.querySelector('.div_content_producto').appendChild(temp_selprod);
        $(temp_selprod).select2({placeholder: 'Producto oferta',dropdownParent: $('#modal-promocion')});
        $(temp_selprod).on("select2:selecting", function(e) {
            if(e.params == undefined){
                action_change_producto(this, this.value);
            }else{
                action_change_producto(this, e.params.args.data.id);
            }
        });
        temp_selprod.parentElement.querySelector('.select2-container').style.width = "100%";
        temp_selprod.parentElement.querySelector('.selection').style.width = "100%";
        var sel_presentacion = div_row.querySelector('.presentacion');
        $(sel_presentacion).select2({placeholder: 'Presentacion', dropdownParent: $('#modal-promocion')});
        sel_presentacion.parentElement.querySelector('.select2-container').style.width = "100%";
        sel_presentacion.parentElement.querySelector('.selection').style.width = "100%";
    }else{
        div_row.insertAdjacentHTML('beforeend', prom_control2);
    }
    var btn_delete = div_row.querySelector('.delete');
    btn_delete.addEventListener('click', action_delete_row);
}

function action_change_producto(obj, new_id) {
    var id_prod = new_id;
    var current_tr = obj.parentElement.parentElement;
    var presentacion_select = current_tr.querySelector('.presentacion');
    var options_length = presentacion_select.options.length;
    var data = [];
    for (var i = 0; i < options_length; i++) {
        presentacion_select.options[0].remove();
    }
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(xhttp.responseText);
        }
    };
    xhttp.open("GET", "/compras/api/presentacionxproducto/" + id_prod, false);
    xhttp.send();
    for (var i = 0; i < data.length; i++) {
        var opt = document.createElement('option');
        opt.value = data[i]['id'];
        opt.innerHTML = data[i]['presentacion']['descripcion'];
        presentacion_select.append(opt)
    }

}

function action_delete_row(){
    this.parentElement.parentElement.remove();
}