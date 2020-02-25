// Variables
let limit, tdocumento;
let xhr = new XMLHttpRequest();
let validatebyNumber = 1;

//Lista de los DOM Elements que se usan:
const dEContentNotifi = document.getElementById('content_notification');
const dENotifi = document.getElementById('notification');
const dEContentTable = document.getElementById('content_table');
const dETbody = document.getElementById('tbody');
const dEInput = document.getElementById('input_documento');
const dESelect = document.getElementById('select_documento');
const dEsContentDocumento = document.getElementsByClassName("content_documento");
const dEsContentNombres = document.getElementsByClassName("content_documento");
const dEsContentApellidos = document.getElementsByClassName("content_documento");

//Inicializa todos los elementos de admisión.
function init_busqueda() {
    tdocumento = 1;
    limit = 8;

    init_busqueda_input();
    init_busqueda_search();
}

// Inicializa el input con evento oninput.
function init_busqueda_input() {
    dEInput.oninput = function(){
        const valor = this.value;
        if(valor.length === limit){
            xhr.open('GET', "/admision/api/search/"+tdocumento+"/"+valor+"/", true);
            xhr.send();

            xhr.onreadystatechange = processPacientData;
        }else{
            dEContentNotifi.classList.add('hide_notification');
            dEContentTable.classList.add('hide_table');
        }
    };
}

// Inicializa el select con evento onchange.
function init_busqueda_search() {
    dESelect.onchange = function () {
        tdocumento = dESelect.options[dESelect.selectedIndex].value;
        if ((tdocumento === 1 || tdocumento === 2) && validatebyNumber !== 1){
            
        }
        limit = parseInt(dESelect.options[dESelect.selectedIndex].getAttribute('data-length'));
        dEInput.setAttribute('maxlength', limit);
        dEInput.value = '';
        dEContentNotifi.classList.add('hide_notification');
        dEContentTable.classList.add('hide_table');
    };
}

// Respuesta al http request de *init_busqueda_input*.
function processPacientData(e) {
   if (xhr.readyState === 4 && xhr.status === 200) {
       const data = JSON.parse(xhr.responseText);
       dEContentNotifi.classList.remove('hide_notification');
       dENotifi.classList.remove('alert-success', 'alert-danger');
       if(data.length>0){
           dENotifi.classList.add('alert-success');
           dENotifi.innerHTML = pacientFound;
           dEContentTable.classList.remove('hide_table');
           dETbody.innerHTML = '';
           for (let i = 0; i < data.length; i++) {
               // TODO change this to dynamically way
                let rowdata = data[i];
                let row = dETbody.insertRow(i);
                let cell_cod = row.insertCell(0);
                cell_cod.innerHTML = rowdata['archivo'];
                let cell_nom = row.insertCell(1);
                cell_nom.innerHTML = rowdata['nombres'];
                let cell_ape = row.insertCell(2);
                cell_ape.innerHTML = rowdata['apellidos'];
                let cell_sex = row.insertCell(3);
                cell_sex.innerHTML = rowdata['edad'];
                let cell_civ = row.insertCell(4);
                cell_civ.innerHTML = rowdata['sexo'];
                let cell_her = row.insertCell(5);
                cell_her.innerHTML = admisionTools;
           }
       }else{
           dENotifi.classList.add('alert-danger');
           dENotifi.innerHTML = pacientNotFound;
       }
    }
}