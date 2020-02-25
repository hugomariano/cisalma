const deletebuttons = document.querySelectorAll('.delete');
const presentacion_to_save = document.getElementById('presentacion_to_save');
const addbutton = document.getElementById('add_btn');
const tr_empty = document.getElementById("tr_presentacion_empty");
const tbody_presentacion = document.getElementById("tbody_presentacion");
const current_pos = document.getElementById("current_pos");
const filtro_form = document.getElementById('filtro_form');

function init_catalogoproveedor_add() {
    init_delete_buttons();
    init_add_button();
    var pos = [];
    for (var i = 1; i <= parseInt(current_pos.value); i++) {
        pos.push(i)
    }
    presentacion_to_save.value=pos.join(',');
}

function init_delete_buttons() {
   for (var i = 0; i < deletebuttons.length; i++) {
        deletebuttons[i].addEventListener("click", action_delete);
   }
}

function action_delete() {
    var id = this.getAttribute("data-id");
    var pos = this.getAttribute("data-pos");
    var tosave = presentacion_to_save.value.split(',');
    for (var i = 0; i < tosave.length; i++) {
        if(tosave[i] == (parseInt(pos)+1)) {
            tosave.splice(i, 1);
        }
    }
    presentacion_to_save.value = tosave.join(',');
    document.getElementById('row_'+pos).remove();

}

function init_add_button() {
    addbutton.addEventListener("click", function () {
        var temp_tr = tr_empty.cloneNode(true);
        temp_tr.removeAttribute("id");
        var select = temp_tr.querySelector("select");
        var pos = (parseInt(current_pos.value) + 1).toString();
        select.setAttribute("name", "p"+pos+"-producto");
        $(select).select2({
          ajax: {
            url: '/maestro/api/producto',
            delay: 250,
            dataType: 'json',
            processResults: function (data) {
                var result = []
                for(var i=0; i<data.length; i++){
                    result.push({'id': data[i].id, 'text': data[i].descripcion});
                }
              return {
                  results: result
              };
            }
          }
        });
        var delete_button = temp_tr.querySelector('.delete');
        current_pos.value = pos;
        delete_button.setAttribute("data-pos", pos);
        delete_button.addEventListener('click', action_delete);
        temp_tr.setAttribute("id", "row_"+pos);
        tbody_presentacion.appendChild(temp_tr);
        $(".select2-container--default").removeAttr('style').css("width","100%");
        if(presentacion_to_save.value === ""){
            presentacion_to_save.value = pos;
        }else{
            var to_save = presentacion_to_save.value.split(',');
            to_save.push(pos);
            presentacion_to_save.value = to_save.join(',');
        }
    });
}
