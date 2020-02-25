var form_pago_venta = document.getElementById('form_pago_venta');
var pago_inp = document.getElementById('pago_inp');
var total_inp = document.getElementById('total_inp');
var cliente_inp = document.getElementById('cliente_inp');
var periodo_credito = document.getElementById('periodo_credito');
var recibo_credito = document.getElementById('recibo_credito');
var descuento_btn = document.querySelectorAll('.descuento_btn');
var form_descuento = document.getElementById('form_descuento');


function init_detail() {

    init_form_pago();
    init_tipo_pago_change();
    init_descuento_btn();
    pago_inp.value = total_inp.value;
}

function init_form_pago() {
    form_pago_venta.addEventListener('submit', action_form_pago);
}

function init_descuento_btn() {
    for (var i = 0; i < descuento_btn.length; i++) {
        descuento_btn[i].addEventListener("click", action_descuento_btn);
    }
}

function action_descuento_btn() {
    var id = this.getAttribute('data-id');
    var url = form_descuento.getAttribute('action');
    var url_array = url.split("/");
    url_array[3] = id;
    url = url_array.join("/");
    form_descuento.setAttribute('action', url);
}

function action_form_pago(e) {
}

function init_tipo_pago_change() {
    $('.tipo_pago').on("select2:selecting", function(e) {
        action_tipo_pago(this, e.params.args.data.id);
    });
}
function action_tipo_pago(obj, new_value) {
    if(new_value === '1'){
        pago_inp.setAttribute('readonly', 'readonly');
        pago_inp.value = total_inp.value;
        periodo_credito.classList.add("periodo_credito_hdn");
        recibo_credito.classList.add("periodo_credito_hdn");
    }else if(new_value==='2'){
        if(cliente_inp.value === ''){
            obj.value = '1';
            $(obj).trigger('select2:selecting');
        }else{
            pago_inp.removeAttribute("readonly");
            pago_inp.value = '';
            periodo_credito.classList.remove("periodo_credito_hdn");
            recibo_credito.classList.remove("periodo_credito_hdn");
        }
    }
}