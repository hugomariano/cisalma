var form_pago_compra = document.getElementById('form_pago_compra');
var pago_inp = document.getElementById('pago_inp');
var total_inp = document.getElementById('total_inp');
var periodo_credito = document.getElementById('periodo_credito');
var recibo_credito = document.getElementById('recibo_credito');

function init_detail() {

    init_form_pago();
    init_tipo_pago_change();
    pago_inp.value = total_inp.value;
}

function init_form_pago() {
    form_pago_compra.addEventListener('submit', action_form_pago);
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
            pago_inp.removeAttribute("readonly");
            pago_inp.value = '';
            periodo_credito.classList.remove("periodo_credito_hdn");
            recibo_credito.classList.remove("periodo_credito_hdn");
    }
}