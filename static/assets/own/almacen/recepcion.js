var cantidad_pedido = document.querySelectorAll('.cantidad_pedido');
var cantidad_entrega = document.querySelectorAll('.cantidad_entrega');
var total = document.querySelectorAll('.totalfinal');
var producto = document.querySelector('.producto_nopedido');
var presentacionxproducto = document.querySelector('.presentacionxproducto_nopedido');
var cantidad_presentacion_entrega = document.querySelector('.cantidad_presentacion_entrega_nopedido');
var total_final = document.querySelector('.total_final_nopedido');
var btn_nopedido = document.querySelector('.agregar_nopedido');
var tr_empty = document.getElementById("tr_nopedido_empty");
var tbody_nopedido = document.getElementById("tbody_nopedido");
var current_pos = document.getElementById("current_pos");
var detallecompra_to_save = document.getElementById('detallecompra_to_save');
var detallecompra_to_delete = document.getElementById('detallecompra_to_delete');

function init_recepcion() {
    var pos = [];
    for (var i = 1; i <= parseInt(current_pos.value); i++) {
        pos.push(i);
    }
    var list_pos = pos.join(',');
    detallecompra_to_save.value=list_pos;
    init_cantidad_entrega_blur();
    init_totalfinal_blur();
    init_prod_change();
    init_btn_nopedido();
    init_delete_button();
}

function init_cantidad_entrega_blur() {
    for (var i = 0; i < cantidad_entrega.length; i++) {
        cantidad_entrega[i].addEventListener("blur", action_cantidad_entrega_blur);
        var event = new Event('blur');
        cantidad_entrega[i].dispatchEvent(event);
    }
}

function init_totalfinal_blur() {
    for (var i = 0; i < total.length; i++) {
        total[i].addEventListener("blur", action_totalfinal_blur);
    }
}

function init_prod_change() {
    $('.producto_nopedido').on("select2:selecting", function(e) {
       prod_change(this, e.params.args.data.id,e);
    });
}

function init_btn_nopedido() {
    btn_nopedido.addEventListener("click", action_btn_nopedido);
}

function init_delete_button() {
    var delete_btns = document.getElementsByClassName('delete');
    for (var i = 0; i < delete_btns.length; i++) {
        delete_btns[i].addEventListener('click', action_delete);
    }
}

function action_cantidad_entrega_blur() {
    var tr_content = this.parentElement.parentElement;
    var is_oferta = tr_content.querySelector('.is_oferta');
    var is_nodeseado = tr_content.querySelector('.is_nodeseado');
    var totalfinal = tr_content.querySelector('.totalfinal');
    // El empty que se usa para clonar no pasará la condición, las filas sí.
    if(is_oferta !== null && is_nodeseado !== null){
        if(is_nodeseado.value === 'False') {
            var current_cantidad_pedido = tr_content.querySelector('.cantidad_pedido');
            var color = get_color_cantidad(parseInt(current_cantidad_pedido.value), parseInt(this.value));
            this.style.backgroundColor = color;
        }
        if(is_oferta.value === 'False' || is_nodeseado.value === 'True'){
            var td_descuento = tr_content.querySelector('.td_descuento');
            if (td_descuento === null ){
                var descuento = 0;
            }else{
                var descuento = td_descuento.innerHTML;
            }
            var td_precio = tr_content.querySelector('.td_precio');
            //td_precio.innerHTML = cortarNumero((parseFloat(totalfinal.value)+parseFloat(descuento))/parseFloat(this.value), 2);
        }
    }
    var event = new Event('blur');
    totalfinal.dispatchEvent(event);
}

function cortarNumero(num, fixed) {
    var re = new RegExp('^-?\\d+(?:\.\\d{0,' + (fixed || -1) + '})?');
    return num.toString().match(re)[0];
}

function get_color_cantidad(pedido, entrega) {
    var color = '';
    if(pedido == entrega){
        color = '#b3e6e6';
    }else if(pedido > entrega){
        color = '#ffcdcc';
    }else{
        color = '#FACE8D';
    }
    return color;
}



function action_totalfinal_blur() {
    var tr_content = this.parentElement.parentElement;
    var current_cantidad_pedido = tr_content.querySelector('.cantidad_entrega');
    var td_descuento = tr_content.querySelector('.td_descuento');
    var impuesto_inp = tr_content.querySelector('.impuesto_inp');
    var total_final_inp = tr_content.querySelector('.totalfinal');
    if (td_descuento === null ){
        var descuento = 0;
    }else{
        var descuento = td_descuento.innerHTML;
    }
    var total = ((parseFloat(total_final_inp.value)*100)/(100+parseFloat(impuesto_inp.value)));
    var td_precio = tr_content.querySelector('.td_precio');
    td_precio.innerHTML = cortarNumero((total+parseFloat(descuento))/parseFloat(current_cantidad_pedido.value), 2);
}

function prod_change(obj, new_value,e) {
    var id_prod = new_value;
    var options_length = presentacionxproducto.options.length;
    var data = [];
    for (var i = 0; i < options_length; i++) {
        presentacionxproducto.options[0].remove();
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
        presentacionxproducto.append(opt);
    }
    presentacionxproducto.value = '';
    $(presentacionxproducto).select2('open');
}

function action_btn_nopedido() {
    var pos = (parseInt(current_pos.value) + 1).toString();
    var producto_text = producto.options[producto.selectedIndex].text;
    var producto_val = producto.value;
    var presentacionxproducto_text = presentacionxproducto.options[presentacionxproducto.selectedIndex].text;
    var presentacionxproducto_val = presentacionxproducto.value;
    var cantidad_presentacion_entrega_val = cantidad_presentacion_entrega.value;
    var total_final_val = total_final.value;
    var precio_val = cortarNumero(parseFloat(total_final_val)/cantidad_presentacion_entrega_val, 2);
    var temp_tr = tr_empty.cloneNode(true);
    var input_id = document.createElement("input");
    input_id.setAttribute("type", "hidden");
    input_id.setAttribute("name", "dc"+pos+"-id");
    var input_prod = document.createElement("input");
    input_prod.setAttribute("type", "hidden");
    input_prod.setAttribute("name", "dc"+pos+"-producto");
    input_prod.setAttribute("value", producto_val);
    var input_pres = document.createElement("input");
    input_pres.setAttribute("type", "hidden");
    input_pres.setAttribute("name", "dc"+pos+"-presentacionxproducto");
    input_pres.setAttribute("value", presentacionxproducto_val);
    temp_tr.removeAttribute("id");
    temp_tr.querySelector(".td_producto").innerHTML = producto_text;
    temp_tr.querySelector(".td_producto").appendChild(input_id);
    temp_tr.querySelector(".td_producto").appendChild(input_prod);
    temp_tr.querySelector(".td_presentacion").innerHTML = presentacionxproducto_text;
    temp_tr.querySelector(".td_presentacion").appendChild(input_pres);
    temp_tr.querySelector(".cantidad_entrega").value = cantidad_presentacion_entrega_val;
    temp_tr.querySelector(".cantidad_entrega").setAttribute("name", "dc"+pos+"-cantidad_presentacion_entrega");
    temp_tr.querySelector(".cantidad_entrega").addEventListener('blur', action_cantidad_entrega_blur);
    temp_tr.querySelector(".td_precio").innerHTML = precio_val;
    temp_tr.querySelector(".totalfinal").value = total_final_val;
    temp_tr.querySelector(".totalfinal").setAttribute("name", "dc"+pos+"-total_final");
    temp_tr.querySelector(".totalfinal").addEventListener('blur', action_totalfinal_blur);
    var delete_button = temp_tr.querySelector('.delete_hdn');
    current_pos.value = pos;
    delete_button.addEventListener('click', action_delete);
    temp_tr.setAttribute("id", "tr_dc_"+pos);
    if(detallecompra_to_save.value === ""){
        detallecompra_to_save.value = pos;
    }else{
        var to_save = detallecompra_to_save.value.split(',');
        to_save.push(pos);
        detallecompra_to_save.value = to_save.join(',');
    }
    tbody_nopedido.appendChild(temp_tr);
    $('#modal-agregar_producto').modal('hide');

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