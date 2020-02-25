var proveedor_id = document.getElementById('proveedor_id').value;
var detallecompra_to_save = document.getElementById('detallecompra_to_save');
var detallecompra_to_delete = document.getElementById('detallecompra_to_delete');
var current_pos = document.getElementById("current_pos");
var addbutton = document.getElementById("add_btn");
var tr_empty = document.getElementById("tr_detallecompra_empty");
var tbody_detallecompra = document.getElementById("tbody_detallecompra");
var btn_add_promocion = document.getElementById('add_promocion');
var btn_save_promocion = document.getElementById('save_promocion');
var btn_save_impuesto = document.getElementById('save_impuesto');
var div_promocion_empty = document.getElementById('div_promocion_empty');
var body_promociones = document.getElementById('body_promociones');
var div_producto_empty = document.getElementById('div_producto_empty');
var btn_promocion = document.querySelectorAll('.promocion');
var current_pos_promocion = document.getElementById('current_pos_promocion');
var impuesto_select = document.getElementById('id_impuesto');
var current_pos_impuesto = document.getElementById('current_pos_impuesto');
var compra_total = document.getElementById('compra_total');


function init_compraedit() {
    var pos = [];
    var prod = [];
    var data = [];
    for (var i = 1; i <= parseInt(current_pos.value); i++) {
        var tr = document.getElementById('tr_dc_'+i);
        var prod_select = tr.querySelector('.producto');
        var prod_value = prod_select.value;
        prod_select.removeAttribute('id');
        prod_select.setAttribute('data-pos', i);
        pos.push(i);
        prod.push(prod_value);
    }
    var list_pos = pos.join(',');
    var list_prod = prod.join(',');
    detallecompra_to_save.value=list_pos;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           data = JSON.parse(xhttp.responseText);
        }
    };
    if(list_prod !== ''){
        xhttp.open("GET", "/compras/api/presentacionxproducto/"+list_prod, false);
        xhttp.send();
    }
    init_save_impuesto_button();
    init_presentacion_select(data);
    init_cant_blur();
    init_controllers();
    init_prod_change();
    init_pres_change();
    init_precio_blur();
    init_add_button();
    init_delete_button();
    init_keypress();
    init_promocion_button();
    init_addpromocion_button();
    init_save_promocion_button();
    init_tax_button();
}

function init_save_impuesto_button() {
    btn_save_impuesto.addEventListener('click', function () {
        var current_pos = current_pos_impuesto.value;
        var current_tr  = document.getElementById('tr_dc_'+current_pos);
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
        if(current_values.length > 0){
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
        }else{
            var temp_btn = document.createElement("button");
            temp_btn.classList.add("btn");
            temp_btn.classList.add("btn-xs");
            temp_btn.classList.add("btn-success");
            temp_btn.classList.add("tax");
            temp_btn.setAttribute('type', 'button');
            var temp_i = document.createElement("i");
            temp_i.classList.add("fa");
            temp_i.classList.add("fa-plus");
            temp_i.classList.add("fas");
            temp_btn.appendChild(temp_i);
            temp_btn.addEventListener("click", action_tax_button);
            td_impuesto.appendChild(temp_btn);
        }
        action_calcular_line_total(current_tr, '');
        $('#modal-impuesto').modal('hide');
    });
}
function init_presentacion_select(data) {
    for (var i = 0; i < data.length; i++) {
        var opt = document.createElement('option');
        opt.value = data[i]['id'];
        opt.innerHTML = data[i]['presentacion']['descripcion'];
        var select = document.getElementById('sel_pre_'+data[i]['producto']);
        select.append(opt)
    }
    var selects = document.getElementsByClassName('sel_presentacionxproducto');
    for (var i = 0; i < selects.length; i++){
        var selected = selects[i].getAttribute("data-selected");
        selects[i].value=selected;
        $(selects[i]).select2();
    }
    $(".select2-container--default").removeAttr('style').css("width","100%");
}
function init_controllers() {
    for (var i = 1; i <= parseInt(current_pos.value); i++) {
        var tr = document.getElementById('tr_dc_'+i);
        var cantidad_inp = tr.querySelector('.cantidadpresentacion');
        var event = new Event('blur');
        cantidad_inp.dispatchEvent(event);
        var impuestos = tr.querySelector('.impuesto_inp').value;
        if (impuestos !== '' && impuestos !== '[]') {
            current_pos_impuesto.value = tr.querySelector('.tax').getAttribute("data-pos");
            impuestos = JSON.parse(impuestos);
            $(impuesto_select).val(impuestos).change();
            var event = new Event('click');
            btn_save_impuesto.dispatchEvent(event);
        }
        var ofertas = tr.querySelector('.promocion_inp').value;
        if (ofertas !== '' && ofertas !== '[]') {
            tr.querySelector('.promocion').classList.remove("btn-default");
            tr.querySelector('.promocion').classList.add("btn-info");
        }
    }
}
function init_prod_change() {
    $('.producto').on("select2:selecting", function(e) {
       prod_change(this, e.params.args.data.id,e);
    });
}
function init_pres_change() {
    $('.sel_presentacionxproducto').on("select2:selecting", function(e) {
       action_pres_change(this, e.params.args.data.id);
    });
}

function init_cant_blur() {
    var cant = document.querySelectorAll('.cantidadpresentacion');
    for (var i = 0; i < cant.length; i++) {
        cant[i].addEventListener("blur", action_cant_blur);
    }
}
function init_precio_blur() {
    var cant = document.querySelectorAll('.precio');
    for (var i = 0; i < cant.length; i++) {
        cant[i].addEventListener("blur", action_cant_blur);
    }
}
function action_cant_blur() {
    var tr = this.parentElement.parentElement;
    action_calcular_line_total(tr, '');
    var total = 0;
    for (var i = 1; i <= parseInt(current_pos.value); i++) {
        var tr_for = document.getElementById('tr_dc_'+i);
        var td_total = tr_for.querySelector('.td_total');
        total += parseFloat(td_total.innerHTML);
    }
    compra_total.innerHTML = total;
}
function prod_change(obj, new_value,e) {
    var id_prod = new_value;
    if(!validar_duplicado_prod(id_prod)) {
        var current_tr = document.getElementById('tr_dc_' + obj.getAttribute('data-pos'));
        var presentacion_select = current_tr.querySelector('.sel_presentacionxproducto');
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
            opt.innerHTML = data[i]['presentacion']['descripcion'] + ' x ' + data[i]['cantidad'] + 'U.';
            presentacion_select.append(opt);
        }
        presentacion_select.value = '';
        $(presentacion_select).select2('open');
    }else{
        alert('No se puede duplicar productos.');
        e.preventDefault();
    }
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
    var data = [];
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(xhttp.responseText);
            if(data.length === 0){
                data[0] = {};
                data[0]['precio_tentativo'] = 0;
            }
        }
    };
    xhttp.open("GET", "/compras/api/preciotentativo/"+new_value, false);
    xhttp.send();
    var tr = obj.parentElement.parentElement;
    tr.querySelector('.precio').value = data[0]['precio_tentativo'];
    var cantidad = tr.querySelector('.cantidadpresentacion').value;
    if(cantidad != ''){
        var total = data[0]['precio_tentativo']*cantidad;
        tr.querySelector('.td_total').innerHTML = total;
        action_calcular_total();
    }
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
        var precio = temp_tr.querySelector(".precio");
        cantidad_presentacion.addEventListener('keypress', function (e) {
            if(e.keyCode == 13){
                setTimeout(function(){$(precio).focus();},0);
                e.preventDefault();
            }
        });
        var pos = (parseInt(current_pos.value) + 1).toString();
        var promocion = temp_tr.querySelector(".promocion");
        var promocion_inp = temp_tr.querySelector(".promocion_inp");
        var tax = temp_tr.querySelector('.tax');
        var tax_inp = temp_tr.querySelector('.impuesto_inp');
        tax.addEventListener("click", action_tax_button);
        tax.setAttribute('data-pos', pos);
        promocion_inp.setAttribute('name', 'dc'+pos+'-oferta');
        tax_inp.setAttribute('name', 'dc'+pos+'-impuesto');
        promocion.setAttribute('data-pos', pos);
        promocion.addEventListener('click', action_btn_promocion);
        select.removeAttribute('name');
        select.setAttribute('name', 'dc'+pos+'-producto');
        select.setAttribute('data-pos', pos);
        select.setAttribute('required', 'required');
        cantidad_presentacion.setAttribute('required', 'required');
        cantidad_presentacion.addEventListener("blur", action_cant_blur);
        cantidad_presentacion.removeAttribute('name');
        cantidad_presentacion.setAttribute('name', 'dc'+pos+'-cantidad_presentacion_pedido');
        precio.setAttribute('required', 'required');
        precio.addEventListener("blur", action_cant_blur);
        precio.removeAttribute('name');
        precio.setAttribute('name', 'dc'+pos+'-precio');
        select_presentacion.classList.add('sel_presentacionxproducto');
        select_presentacion.setAttribute('required', 'required');
        select_presentacion.removeAttribute('name');
        select_presentacion.setAttribute('name', 'dc'+pos+'-presentacionxproducto');
        $(select_presentacion).select2({placeholder: "Seleccione el Producto"});
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
        temp_tr.setAttribute("id", "tr_dc_"+pos);
        tbody_detallecompra.appendChild(temp_tr);
        $(".select2-container--default").removeAttr('style').css("width","100%");
        if(detallecompra_to_save.value === ""){
            detallecompra_to_save.value = pos;
        }else{
            var to_save = detallecompra_to_save.value.split(',');
            to_save.push(pos);
            detallecompra_to_save.value = to_save.join(',');
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
   var current_delete = detallecompra_to_delete.value;
   var current_save = detallecompra_to_save.value;
   var array_save = current_save.split(',');
   if(data_id != null){
        if(current_delete === ''){
            detallecompra_to_delete.value = data_id;
        }else{
            var array_delete = current_delete.split(',');
            array_delete.push(data_id);
            detallecompra_to_delete.value = array_delete.join(',');
        }
   }
    for (var i = 0; i < array_save.length; i++) {
        if(array_save[i] === pos) {
            array_save.splice(i, 1);
        }
    }
    detallecompra_to_save.value = array_save.join(',');
    document.getElementById('tr_dc_'+pos).remove();
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
function action_calcular_line_total(tr, value) {
    var cantidad = tr.querySelector('.cantidadpresentacion').value;
    var precio = tr.querySelector('.precio').value;
    var impuesto = tr.querySelector('.impuesto_inp').value;
    if(tr.querySelector('.promocion_inp').value !== ''){
        var oferta = JSON.parse(tr.querySelector('.promocion_inp').value);
    }else{
        var oferta = [];
    }
    var descuento = 0;
    var td_descuento = tr.querySelector('.td_descuento');
    var current_cantidad_presentacion;
    var presentacionxproducto = tr.querySelector('.sel_presentacionxproducto');
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
            var temp_ofer = oferta[i];
            if (temp_ofer[0] === '2' || temp_ofer[0] === '3'){
                var ofer_retorno = parseFloat(temp_ofer[2]);
                var ofer_cantidad_unitaria =  parseFloat(temp_ofer[1]);;
                var current_cantidad_unitaria = parseFloat(cantidad);
                if (temp_ofer[0] === '2'){
                    descuento += (Math.floor(current_cantidad_unitaria/ofer_cantidad_unitaria)*ofer_retorno)
                }else if(temp_ofer[0] === '3' && current_cantidad_unitaria>=ofer_cantidad_unitaria){
                    descuento += ((subtotal*ofer_retorno)/100)
                }
             }
        }
        tr.querySelector('.td_subtotal').innerHTML = subtotal.toFixed(2);
        td_descuento.innerHTML = descuento.toFixed(2);
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
function action_calcular_total() {
    var td_total = document.querySelectorAll('.td_total');
    var total = 0;
    for(var i = 0; i < td_total.length; i++){
        total += parseFloat(td_total[i].innerHTML);
    }
    document.getElementById('compra_total').innerHTML = total;
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
    if(pos != current_pos){
        var row = body_promociones.querySelectorAll('.form-inline');
        for (var i =1; i < row.length; i++) {
            row[i].remove();
        }
        var current_tr  = document.getElementById('tr_dc_'+pos);
        var promocion_inp = current_tr.querySelector('.promocion_inp');
        if(promocion_inp.value != '') {
            var promociones = JSON.parse(promocion_inp.value);
            for (var i = 0; i < promociones.length; i++) {
                var event_click = new Event('click');
                btn_add_promocion.dispatchEvent(event_click);
                var row = body_promociones.querySelectorAll('.form-inline');
                $(row[i+1].querySelector('.tipo_promocion')).val(promociones[i][0]).trigger('change').trigger('select2:selecting');
                row[i+1].querySelector('.cantidad').value = promociones[i][1];
                row[i+1].querySelector('.retorno').value = promociones[i][2];
                $(row[i+1].querySelector('.producto')).val(promociones[i][3]).trigger('change').trigger('select2:selecting');
                $(row[i+1].querySelector('.presentacion')).val(promociones[i][4]).trigger('change').trigger('select2:selecting');
            }
        }
    }
    $('#modal-promocion').modal('show');
    current_pos_promocion.value = pos;

}

function init_addpromocion_button() {
    btn_add_promocion.addEventListener('click', function () {
        var temp_div = div_promocion_empty.cloneNode(true);
        temp_div.removeAttribute("id");
        var select_tipo_promocion = temp_div.querySelector('.tipo_promocion');
        $(select_tipo_promocion).select2({placeholder: "Tipo de Promocion", dropdownParent: $('#modal-promocion')});
        temp_div.querySelector('.select2-container').style.width = "100%";
        temp_div.querySelector('.selection').style.width = "100%";
        $(select_tipo_promocion).on("select2:selecting", function(e) {
            if(e.params == undefined){
                action_change_tipoprom(this, this.value);
            }else{
                action_change_tipoprom(this, e.params.args.data.id);
            }
        });
        body_promociones.appendChild(temp_div);
    });
}

function init_save_promocion_button() {
    btn_save_promocion.addEventListener('click', function () {
        var array_content = [];
        var body_promociones = document.getElementById('body_promociones');
        var row = body_promociones.querySelectorAll('.form-inline');
        for (var i =1; i < row.length; i++){
            var temp_array = [];
            var tipo_prom = row[i].querySelector('.tipo_promocion').value;
            var cantidad = row[i].querySelector('.cantidad').value;
            var retorno = row[i].querySelector('.retorno').value;
            temp_array = temp_array.concat([tipo_prom, cantidad, retorno]);
            if (tipo_prom === "1"){
                var producto = row[i].querySelector('.producto').value;
                var presentacion = row[i].querySelector('.presentacion').value;
                temp_array = temp_array.concat([producto, presentacion]);
            }
            array_content.push(temp_array);
        }
        var current_pos = current_pos_promocion. value;
        var current_tr  = document.getElementById('tr_dc_'+current_pos);
        var string_promocion = JSON.stringify(array_content);
        current_tr.querySelector('.promocion_inp').value = string_promocion;
        if(string_promocion == '[]'){
            current_tr.querySelector('.promocion').classList.remove("btn-info");
            current_tr.querySelector('.promocion').classList.add("btn-default");
        }else{
            current_tr.querySelector('.promocion').classList.remove("btn-default");
            current_tr.querySelector('.promocion').classList.add("btn-info");
        }
        var cantidad_inp = current_tr.querySelector('.cantidadpresentacion');
        var event = new Event('blur');
        cantidad_inp.dispatchEvent(event);
        $('#modal-promocion').modal('hide');
    });
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

function action_delete_row(){
    this.parentElement.parentElement.remove();
}