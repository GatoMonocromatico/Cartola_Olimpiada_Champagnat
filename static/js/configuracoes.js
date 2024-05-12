const button = document.getElementById("btn_submit");
const blurr = document.getElementById("blur");
const inputs = document.getElementsByTagName("input");
const popUp = document.getElementById("popUp");
const form = document.getElementById("form");
const voltarIndex = document.getElementById("voltar_index");
const sairAviso = document.getElementById("sair_aviso");

button.addEventListener("click", () => {
    blurr.style.filter = "blur(10px)";
    popUp.style.transform = "translate(-50%, -50%) scale(1)"
    popUp.style.visibility = "visible"
})
voltarIndex.addEventListener("click", () => {
    window.location.href = "/"
})
sairAviso.addEventListener("click",()=>{
    blurr.style.filter = "blur(0px)";
    popUp.style.transform = "translate(-50%, 0) scale(0)"
    popUp.style.visibility = "hidden"
})

const btnSubmit = $("#submit")
const inpFotoDePerfil = $("#inp_foto_perfil")
const foto = $("#profile-picture")

const inpNaoJogador = $("#nao_jogador")
const inpEsporte1Form = $("#esporte1_form")
const inpEsporte2Form = $("#esporte2_form")
const inpPosicao1Form = $("#input_posicao_esporte1_form")
const inpPosicao2Form = $("#input_posicao_esporte2_form")

const inpModalidadeFeminina = $("#modalidade_feminina")
const inpModalidadeMasculina = $("#modalidade_masculina")

const fieldset = $("#myfieldset")

$(".input_esporte").on("change", function(){
    if (inpNaoJogador.is(":checked")) {
        $("#esporte1").prop("checked", false)
        $("#esporte2").prop("checked", false)
        $("#input_posicao_esporte1").prop("checked", false)
        $("#input_posicao_esporte2").prop("checked", false)
        $(".div_input_esporte").remove()
        $("#legenda").remove()
        fieldset.css("border", "none")
    }
    else {
        if ($(".div_input_esporte").length == 0) {
            fieldset.css("border", "3px solid #0F3B5E")
            fieldset.append(`
            <legend id="legenda" style="font-family: 'Open Sans', sans-serif; font-weight: bold; color: #0f3b5e">Esportes:</legend>
            
            <div class="mod_checkbox div_input_esporte">
                <input class="inp_esporte_selecionado input_esporte" id="esporte1" name="esportes_selecionados_aparente" value="futsal_feminino" type="checkbox" onchange="atualizar_estado('esporte1')">
                <label id="label_esporte1" for="esporte1">Futsal feminino</label>
            </div>
            <div class="mod_checkbox div_input_esporte" style="display: flex; align-items: center;" id="div_input_posicao_esporte1">
                <a style="font-size: 15px;color:#0f3b5e">-</a>
                <input id="input_posicao_esporte1" type="checkbox" name="goleiro1" value="true" onchange="atualizar_estado('input_posicao_esporte1')"/>
                <label for="input_posicao_esporte1" id="label_posicao">sou goleiro</label>
            </div> 
            <div class="mod_checkbox div_input_esporte">
                <input class="inp_esporte_selecionado input_esporte" id="esporte2" name="esportes_selecionados_aparente" value="handebol" type="checkbox" onchange="atualizar_estado('esporte2')">
                <label id="label_esporte2" for="esporte2">Handebol</label>
            </div>
            <div class="mod_checkbox div_input_esporte" style="display: flex; align-items: center;" id="div_input_posicao_esporte2">
                <a style="font-size: 15px;color:#0f3b5e">-</a>
                <input id="input_posicao_esporte2" type="checkbox" name="goleiro2" value="true" onchange="atualizar_estado('input_posicao_esporte2')"/>
                <label for="input_posicao_esporte2" id="label_posicao">sou goleiro</label>
            </div>`)


        } else if ($(".div_input_esporte").length == 3) {
            fieldset.append(`
            <div class="mod_checkbox div_input_esporte" style="display: flex; align-items: center;" id="div_input_posicao_esporte2">
                <a style="font-size: 15px;color:#0f3b5e">-</a>
                <input id="input_posicao_esporte2" type="checkbox" name="goleiro2" value="true" onchange="atualizar_estado('input_posicao_esporte2')"/>
                <label for="input_posicao_esporte2" id="label_posicao">sou goleiro</label>
            </div>`)
        }

        let input = $( this )
        let id = input.attr("id")
        if (id == "modalidade_masculina") {
            $("#label_esporte1").html("Futsal masculino")
            $("#label_esporte2").html("Basquete")
            $("#div_input_posicao_esporte2").remove()
            inpEsporte1Form.attr("value", "futsal_masculino")
            inpEsporte2Form.attr("value", "basquete")
            inpPosicao1Form.attr("value", "futsal_masculino")
            atualizar_estado(id)
        }
        else if (id == "modalidade_feminina") {
            $("#label_esporte1").html("Futsal feminino")
            $("#label_esporte2").html("Handebol")
            inpEsporte1Form.attr("value", "futsal_feminino")
            inpEsporte2Form.attr("value", "handebol")
            inpPosicao1Form.attr("value", "futsal_feminino")
            $("#esporte2").prop("disabled", false)
            atualizar_estado(id)
        }        
    }
})

function atualizar_estado(id) {
    let input = $("#" + id)
    let checkar = false
    if (input.is(":checked")) {
        checkar = true
    }

    if (id == "input_posicao_esporte1") {
        inpPosicao1Form.prop("checked", checkar)
        inpPosicao1Form.trigger("change")
    }
    else if (id == "input_posicao_esporte2") {
        inpPosicao2Form.prop("checked", checkar)
        inpPosicao2Form.trigger("change")
    }
    else if (id == "esporte1") {
        inpEsporte1Form.prop("checked", checkar)            
    }
    else if (id == "esporte2") {
        inpEsporte2Form.prop("checked", checkar)    
    }
}

btnSubmit.on("click", () => {
    $('#myform').trigger("submit")
})

$('#myform').on("submit", function(event) {
    event.preventDefault();

    let checkeboxes = $(".inp_esporte_selecionado:checked")
    if (checkeboxes.length < 1 && !inpNaoJogador.is(":checked") && naoCadastrouEsportes) {
        alert("Selecione pelo menos uma opção de esporte ou se não for cadastrar-se como jogador(a) selecione a opção 'Não sou um jogador(a)'")
    } else {
        let arquivo = inpFotoDePerfil[0].files[0];        
        // Crie um objeto FormData
        let formData = new FormData();

        // Adicione o arquivo ao objeto FormData
        formData.append('imagem', arquivo);
        
        if (arquivo) {
            formData.append("tem_imagem", true)
        } else {
            formData.append("tem_imagem", false)
        }

        if (naoCadastrouEsportes) {
            let modalidade
            let esportes_selecionados = []
            if (inpModalidadeFeminina.is(":checked")) {
                modalidade = "F"
            }
            else if (inpModalidadeMasculina.is(":checked")) {
                modalidade = "M"
            }
            else {
                modalidade = "E"
            }
            formData.append('modalidade', modalidade);

            if (modalidade != "E") {
                let esporte1 = inpEsporte1Form.val()
                let esporte2 = inpEsporte2Form.val()

                if (inpEsporte1Form.is(":checked")) {
                    esportes_selecionados.push(esporte1)
                    console.log("esporte1" + esporte1)
                }
                if (inpEsporte2Form.is(":checked")) {
                    esportes_selecionados.push(esporte2)
                    console.log("esporte2" + esporte2)
                }
                if (inpPosicao1Form.is(":checked")) {
                    formData.append(`gol_${esporte1}`, "true");
                }
                if (inpPosicao2Form.is(":checked")) {
                    formData.append(`gol_${esporte2}`, "true");
                }
                formData.append('esportes_selecionados', esportes_selecionados);
                console.log(esportes_selecionados)
            }
        }
        console.log(formData.get('esportes_selecionados'))

        // Configurar a solicitação AJAX
        $.ajax({
            url: '/configurações',
            type: 'POST',
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            success: function(response) {
                window.location.reload();
            },
            error: function(xhr, status, error) {
                console.error('Erro ao enviar imagem:', error);
            }
        });
    }
  });

inpFotoDePerfil.on("change", () => {
    const file = inpFotoDePerfil[0].files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = foto.attr('src', e.target.result);
            foto.css('width', '80px');
        }
        reader.readAsDataURL(file);
        foto.css("box-shadow", "-4px 4px 0px 0px #515151")
    }
})