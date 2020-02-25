var div_producto_retorno = document.getElementById('div_producto_retorno');
var div_limite = document.getElementById('div_limite');

function init_ofertaedit() {
    init_tipo_change();
    init_duracion_change();
}

function init_tipo_change() {
    $('#id_tipo').on("select2:selecting", function(e) {
       action_tipo_change(this, e.params.args.data.id);
    });
}

function action_tipo_change(obj, new_value) {
    if(new_value === '1'){
        div_producto_retorno.style.display = 'flex';
    }else if(new_value === '2' || new_value === '3'){
        div_producto_retorno.style.display = 'none';
    }
}

function init_duracion_change() {
    $('#id_tipo_duracion').on("select2:selecting", function(e) {
       action_duracion_change(this, e.params.args.data.id);
    });
}

function action_duracion_change(obj, new_value) {
    if(new_value === '1'){
        div_limite.style.display = 'flex';
    }else if(new_value === '2' || new_value === '3'){
        div_limite.style.display = 'none';
    }
}