var tipo_comprobante_select = document.getElementById('id_tipo_comprobante');
var serie_comprobante_inp = document.getElementById('id_serie_comprobante');
var numero_comprobante_inp = document.getElementById('id_numero_comprobante');

function init_ordencompradetail() {
    init_estado_envio();
}

function init_estado_envio(){
    $('#id_estado_envio').on("select2:selecting", function(e) {
       action_estado_envio_change(this, e.params.args.data.id);
    });
}

function action_estado_envio_change(obj, new_value) {
    if(new_value === '1'){
        tipo_comprobante_select.removeAttribute("required");
        serie_comprobante_inp.removeAttribute("required");
        numero_comprobante_inp.removeAttribute("required");
    }else if(new_value === '2'){
        tipo_comprobante_select.setAttribute("required", "required");
        serie_comprobante_inp.setAttribute("required", "required");
        numero_comprobante_inp.setAttribute("required", "required");
    }
}