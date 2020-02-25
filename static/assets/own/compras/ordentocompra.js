var inp_precio = document.querySelectorAll('.precio');
var td_total = document.querySelectorAll('.td_total');
var td_total_compra = document.getElementById('total');
var btn_add_promocion = document.getElementById('add_promocion');
var btn_save_promocion = document.getElementById('save_promocion');
var div_promocion_empty = document.getElementById('div_promocion_empty');
var body_promociones = document.getElementById('body_promociones');
var div_producto_empty = document.getElementById('div_producto_empty');
var btn_promocion = document.querySelectorAll('.promocion');
var current_pos_promocion = document.getElementById('current_pos_promocion');

function init_ordentocompra() {
    init_precio_blur();
    init_promocion_button();
    init_add_button();
    init_save_promocion_button();
}

function init_precio_blur() {
    for (var i =0; i < inp_precio.length; i++){
        inp_precio[i].addEventListener('blur', action_actualizar_total);
    }
}

function init_promocion_button() {
    for (var i =0; i < btn_promocion.length; i++){
        btn_promocion[i].addEventListener('click', action_btn_promocion);
    }
}

function action_btn_promocion() {
    var pos = this.getAttribute('data-pos');
    var current_pos = current_pos_promocion.value;
    if(current_pos != '' && pos != current_pos){
        var row = body_promociones.querySelectorAll('.form-inline');
        for (var i =1; i < row.length; i++) {
            row[i].remove();
        }
        var current_tr  = document.getElementById('tr_'+pos);
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

function init_add_button() {
    btn_add_promocion.addEventListener('click', function () {
        var temp_div = div_promocion_empty.cloneNode(true);
        temp_div.removeAttribute("id");
        var select_tipo_promocion = temp_div.querySelector('.tipo_promocion');
        $(select_tipo_promocion).select2({placeholder: "Tipo de Promocion"});
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
        var current_tr  = document.getElementById('tr_'+current_pos);
        current_tr.querySelector('.promocion_inp').value = JSON.stringify(array_content);
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
        div_row.querySelector('.div_content_producto').appendChild(temp_selprod);
        $(temp_selprod).select2({placeholder: 'Producto oferta'});
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
        $(sel_presentacion).select2({placeholder: 'Presentacion'});
        sel_presentacion.parentElement.querySelector('.select2-container').style.width = "100%";
        sel_presentacion.parentElement.querySelector('.selection').style.width = "100%";
    }else{
        div_row.insertAdjacentHTML('beforeend', prom_control2);
    }
    var btn_delete = div_row.querySelector('.delete');
    btn_delete.addEventListener('click', action_delete_row);
}

function action_actualizar_total() {
       var tr = this.parentElement.parentElement;
       var cantidad = tr.querySelector('.cantidad').value;
       var precio = this.value;
       var total = 0;
       tr.querySelector('.td_total').innerHTML = cantidad * precio;
       for (var i =0; i < td_total.length; i++){
           total += parseFloat(td_total[i].innerHTML);
       }
       td_total_compra.innerHTML = total;
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
    const xhttp = new XMLHttpRequest();
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