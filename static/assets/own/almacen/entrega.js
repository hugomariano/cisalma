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
var detalleventa_to_save = document.getElementById('detalleventa_to_save');
var detalleventa_to_delete = document.getElementById('detalleventa_to_delete');

function init_entrega() {
    var pos = [];
    for (var i = 1; i <= parseInt(current_pos.value); i++) {
        pos.push(i);
    }
    var list_pos = pos.join(',');
    detalleventa_to_save.value=list_pos;
    init_cantidad_entrega_blur();
}

function init_cantidad_entrega_blur() {
    for (var i = 0; i < cantidad_entrega.length; i++) {
        cantidad_entrega[i].addEventListener("blur", action_cantidad_entrega_blur);
        var event = new Event('blur');
        cantidad_entrega[i].dispatchEvent(event);
    }
}

function action_cantidad_entrega_blur() {
    var tr_content = this.parentElement.parentElement;
    var is_oferta = tr_content.querySelector('.is_oferta');
    var totalfinal = tr_content.querySelector('.td_total_final');

    var current_cantidad_pedido = tr_content.querySelector('.cantidad_pedido');
    var color = get_color_cantidad(parseInt(current_cantidad_pedido.value), parseInt(this.value));
    this.style.backgroundColor = color;

    var current_cantidad_entrega = tr_content.querySelector('.cantidad_entrega');
    var td_descuento = tr_content.querySelector('.td_descuento');
    var impuesto_inp = tr_content.querySelector('.impuesto_inp');
    var td_precio = tr_content.querySelector('.td_precio');
    var total_final = tr_content.querySelector('.td_total_final');
    if (td_descuento === null ){
        var descuento = 0;
    }else{
        var descuento = parseFloat(td_descuento.innerHTML);
    }
    var total = (parseFloat(current_cantidad_entrega.value)*parseFloat(td_precio.innerHTML)) - descuento;
    total_final.innerHTML = cortarNumero((total+((total*parseFloat(impuesto_inp.value))/100)), 2);
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
