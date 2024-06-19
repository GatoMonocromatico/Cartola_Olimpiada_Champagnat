btnConfig = document.getElementById("icon")

btnConfig.addEventListener("click", () => {
    window.location.href = "/configurações"
})

function hover_btn(idBtn, idDetalhe) {
    let btn = document.getElementsByClassName(idBtn)[0];
    let btnTexto = document.getElementById(idBtn.replace("But", "Text"));

    let detalhe1 = "dtl"+idDetalhe
    let detalhe2 = "dtl"+idDetalhe+"-2"

    btn.style.height = '25%';
    btnTexto.style.color = '#FBB834';
    btnTexto.style.fontSize = '18px';
    document.getElementById(detalhe1).style.opacity = '100%';
    document.getElementById(detalhe2).style.opacity = '100%';
}

function unhover_btn(idBtn, idDetalhe) {
    let btn = document.getElementsByClassName(idBtn)[0];
    let btnTexto = document.getElementById(idBtn.replace("But", "Text"));
    
    let detalhe1 = "dtl"+idDetalhe
    let detalhe2 = "dtl"+idDetalhe+"-2"


    btn.style.height = '15%';
    btnTexto.style.color = '#0F3B5E';
    btnTexto.style.fontSize = '14px';
    document.getElementById(detalhe1).style.opacity = '0%';
    document.getElementById(detalhe2).style.opacity = '0%';

}

const admin = $("#admin")
const trophy = $("#trophy")

admin.on("click", () => {
    window.location.href = "/ADM"
})

trophy.on("click", () => {
    window.location.href = "/leaderboards"
})

// código original abaixo
// código original abaixo
// código original abaixo

const inpFormulario = $("#form_data")
const form = $("#myform")

const blocoEscolherEsporte = $("#bloco_escolha_do_esporte")
const btnEscolheFutsalMasc = "#btn_escolhe_futsal_masc"
const btnEscolheFutsalFem = "#btn_escolhe_futsal_fem"
const btnEscolheBasquete = "#btn_escolhe_basquete"
const btnEscolheHandebol = "#btn_escolhe_handebol"
const btnEscolheEsporteQualquer = ".btn_escolhe_esporte"

var HTMLs = new Map
HTMLs.set("HTML_bloco_escolha_do_esporte", `
<button class="futMascBut btn_escolhe_esporte" id="btn_escolhe_futsal_masc" onmouseenter="hover_btn('futMascBut', '1')" onmouseleave="unhover_btn('futMascBut', '1')" onclick="escalacao('futsal_masculino')">
<img class="btnDetail" id="dtl1" src="static/btnDetail.png">
<a class="futMascText" id="futMascText">Futsal Masculino</a>
<img class="btnDetail2" id="dtl1-2" src="static/btnDetail.png")}}">
</button>
<button class="futFemBut btn_escolhe_esporte" id="btn_escolhe_futsal_fem" onmouseenter="hover_btn('futFemBut', '2')" onmouseleave="unhover_btn('futFemBut', '2')" onclick="escalacao('futsal_feminino')">
<img class="btnDetail" id="dtl2" src="static/btnDetail.png")}}">
<a class="futFemText" id="futFemText" >Futsal Feminino</a>
<img class="btnDetail2" id="dtl2-2" src="static/btnDetail.png")}}">
</button>
<button class="handBut btn_escolhe_esporte" id="btn_escolhe_handebol" onmouseenter="hover_btn('handBut', '3')" onmouseleave="unhover_btn('handBut', '3')" onclick="escalacao('handebol')">
<img class="btnDetail" id="dtl3" src="static/btnDetail.png")}}">
<a class="handText" id="handText">Handebol</a>
<img class="btnDetail2" id="dtl3-2" src="static/btnDetail.png")}}">
</button>
<button class="basketBut btn_escolhe_esporte" id="btn_escolhe_basquete" onmouseenter="hover_btn('basketBut', '4')" onmouseleave="unhover_btn('basketBut', '4')" onclick="escalacao('basquete')">
<img class="btnDetail" id="dtl4" src="static/btnDetail.png")}}">
<a class="basketText" id="basketText">Basquete</a>
<img class="btnDetail2" id="dtl4-2" src="static/btnDetail.png")}}">
</button>`)


//variaveis escolher esporte
const blocoEscalacao = $("#bloco_escalacao")
const btnEscolheJogador = ".btn_escolhe_jogador"
const blocoEscolheJogador = "#bloco_escolhe_jogador"
const btnVoltar = "#btn_voltar_escalacao"

HTMLs.set("HTML_bloco_escalacao_futsal_masculino", `
<div class="escalação_container">
<i class="fa fa-arrow-left simbolo icon2" id="btn_voltar_escalacao" onclick="voltar('bloco_escalacao', 'bloco_escolha_do_esporte')"></i>
<div class="title">
    <p class="esc_title1">
        escalação
    </p>
    <p id="esc_title2" class="esc_title2">
        Futsal Masculino
    </p>
</div>
<div class="container_pontos_e_salvar">
<span id="mercado_fechado"></span>
<div class="pontos_escalacao" style="
    width: 70px;
    padding: 0;
    border-radius: 13px;
    background-color: whitesmoke;
    box-shadow: 0 5px 0 0 #0F3B5E;
    border: 1px solid #0F3B5E;
    text-align: center;
">
<span style="margin: 5px; font-family: 'Open Sans', sans-serif; color: #0F3B5E;">Pontos:</span>
<p style="margin: 5px; font-family: 'Open Sans', sans-serif; color: #0F3B5E;">PONTUACAONOESPORTEATUAL</p>
</div>
<button type="submit" id="btn_salvar" onclick="submit()">Salvar</button>
</div>
<div class="escalações">
    <img src="static/quadra.png" id="quadra" class="escalações_img">
    <button class="goleiroFutMasc escolher_jogador" id="goleiro" onclick="verJogadoresaVenda('goleiro')">+</button>
    <button class="posição1FutMasc escolher_jogador" id="jogador1" onclick="verJogadoresaVenda('jogador1')">+</button>
    <button class="posição2FutMasc escolher_jogador" id="jogador2" onclick="verJogadoresaVenda('jogador2')">+</button>
    <button class="posição3FutMasc escolher_jogador" id="jogador3" onclick="verJogadoresaVenda('jogador3')">+</button>
    <button class="posição4FutMasc escolher_jogador" id="jogador4" onclick="verJogadoresaVenda('jogador4')">+</button>
    <label class="goleiroFutMascText label_escolher_jogador" >Goleiro</label>
    <label class="posicao1FutMascText label_escolher_jogador">Posição 1</label>
    <label class="posicao2FutMascText label_escolher_jogador">Posição 2</label>
    <label class="posicao3FutMascText label_escolher_jogador">Posição 3</label>
    <label class="posicao4FutMascText label_escolher_jogador">Posição 4</label>
</div>
</div>`)

HTMLs.set("HTML_bloco_escalacao_futsal_feminino", `
<div class="escalação_container">
<i class="fa fa-arrow-left simbolo icon2" id="btn_voltar_escalacao" onclick="voltar('bloco_escalacao', 'bloco_escolha_do_esporte')"></i>
<div class="title">
    <p class="esc_title1">
        escalação
    </p>
    <p id="esc_title2" class="esc_title2">
        Futsal Feminino
    </p>
</div>
<div class="container_pontos_e_salvar">
<span id="mercado_fechado"></span>
<div class="pontos_escalacao" style="
    width: 70px;
    padding: 0;
    border-radius: 13px;
    background-color: whitesmoke;
    box-shadow: 0 5px 0 0 #0F3B5E;
    border: 1px solid #0F3B5E;
    text-align: center;
">
<span style="margin: 5px; font-family: 'Open Sans', sans-serif; color: #0F3B5E;">Pontos:</span>
<p style="margin: 5px; font-family: 'Open Sans', sans-serif; color: #0F3B5E;">PONTUACAONOESPORTEATUAL</p>
</div>
<button type="submit" id="btn_salvar" onclick="submit()">Salvar</button>
</div>
<div class="escalações">
    <img src="static/quadra.png" id="quadra" class="escalações_img">
    <button class="goleiroFutFem escolher_jogador" id="goleiro" onclick="verJogadoresaVenda('goleiro')">+</button>
    <button class="posicao1FutFem escolher_jogador" id="jogador1" onclick="verJogadoresaVenda('jogador1')">+</button>
    <button class="posicao2FutFem escolher_jogador" id="jogador2" onclick="verJogadoresaVenda('jogador2')">+</button>
    <button class="posicao3FutFem escolher_jogador" id="jogador3" onclick="verJogadoresaVenda('jogador3')">+</button>
    <button class="posicao4FutFem escolher_jogador" id="jogador4" onclick="verJogadoresaVenda('jogador4')">+</button>
    <label class="goleiroFutFemText label_escolher_jogador" >Goleira</label>
    <label class="posicao1FutFemText label_escolher_jogador">Posição 1</label>
    <label class="posicao2FutFemText label_escolher_jogador">Posição 2</label>
    <label class="posicao3FutFemText label_escolher_jogador">Posição 3</label>
    <label class="posicao4FutFemText label_escolher_jogador">Posição 4</label>
</div>
</div>`)

HTMLs.set("HTML_bloco_escalacao_basquete", `
<div class="escalação_container">
<i class="fa fa-arrow-left simbolo icon2" id="btn_voltar_escalacao" onclick="voltar('bloco_escalacao', 'bloco_escolha_do_esporte')"></i>
<div class="title">
    <p class="esc_title1">
        escalação
    </p>
    <p id="esc_title2" class="esc_title2">
        Basquete
    </p>
</div>
<div class="container_pontos_e_salvar">
<span id="mercado_fechado"></span>
<div class="pontos_escalacao" style="
    width: 70px;
    padding: 0;
    border-radius: 13px;
    background-color: whitesmoke;
    box-shadow: 0 5px 0 0 #0F3B5E;
    border: 1px solid #0F3B5E;
    text-align: center;
">
<span style="margin: 5px; font-family: 'Open Sans', sans-serif; color: #0F3B5E;">Pontos:</span>
<p style="margin: 5px; font-family: 'Open Sans', sans-serif; color: #0F3B5E;">PONTUACAONOESPORTEATUAL</p>
</div>
<button type="submit" id="btn_salvar" onclick="submit()">Salvar</button>
</div>
<div class="escalações">
    <img src="static/quadra.png" id="quadra" class="escalações_img">
    <button class="posicao1Basket escolher_jogador" id="jogador1" onclick="verJogadoresaVenda('jogador1')">+</button>
    <button class="posicao2Basket escolher_jogador" id="jogador2" onclick="verJogadoresaVenda('jogador2')">+</button>
    <button class="posicao3Basket escolher_jogador" id="jogador3" onclick="verJogadoresaVenda('jogador3')">+</button>
    <button class="posicao4Basket escolher_jogador" id="jogador4" onclick="verJogadoresaVenda('jogador4')">+</button>
    <button class="posicao5Basket escolher_jogador" id="jogador5" onclick="verJogadoresaVenda('jogador5')">+</button>
    <label class="posicao1BasketText label_escolher_jogador">Posição 1</label>
    <label class="posicao2BasketText label_escolher_jogador">Posição 2</label>
    <label class="posicao3BasketText label_escolher_jogador">Posição 3</label>
    <label class="posicao4BasketText label_escolher_jogador">Posição 4</label>
    <label class="posicao5BasketText label_escolher_jogador">Posição 5</label>
</div>`)

HTMLs.set("HTML_bloco_escalacao_handebol", `
<div class="escalação_container">
<i class="fa fa-arrow-left simbolo icon2" id="btn_voltar_escalacao" onclick="voltar('bloco_escalacao', 'bloco_escolha_do_esporte')"></i>
<div class="title">
    <p class="esc_title1">
        escalação
    </p>
    <p id="esc_title2" class="esc_title2">
        Handebol
    </p>
</div>
<div class="container_pontos_e_salvar">
<span id="mercado_fechado"></span>
<div class="pontos_escalacao" style="
    width: 70px;
    padding: 0;
    border-radius: 13px;
    background-color: whitesmoke;
    box-shadow: 0 5px 0 0 #0F3B5E;
    border: 1px solid #0F3B5E;
    text-align: center;
">
<span style="margin: 5px; font-family: 'Open Sans', sans-serif; color: #0F3B5E;">Pontos:</span>
<p style="margin: 5px; font-family: 'Open Sans', sans-serif; color: #0F3B5E;">PONTUACAONOESPORTEATUAL</p>
</div>
<button type="submit" id="btn_salvar" onclick="submit()">Salvar</button>
</div>
<div class="escalações">
    <img src="static/quadra.png" id="quadra" class="escalações_img">
    <button class="goleiroHandebol escolher_jogador" id="goleiro" onclick="verJogadoresaVenda('goleiro')">+</button>
    <button class="posicao1Handebol escolher_jogador" id="jogador1" onclick="verJogadoresaVenda('jogador1')">+</button>
    <button class="posicao2Handebol escolher_jogador" id="jogador2" onclick="verJogadoresaVenda('jogador2')">+</button>
    <button class="posicao3Handebol escolher_jogador" id="jogador3" onclick="verJogadoresaVenda('jogador3')">+</button>
    <button class="posicao4Handebol escolher_jogador" id="jogador4" onclick="verJogadoresaVenda('jogador4')">+</button>
    <button class="posicao5Handebol escolher_jogador" id="jogador5" onclick="verJogadoresaVenda('jogador5')">+</button>
    <button class="posicao6Handebol escolher_jogador" id="jogador6" onclick="verJogadoresaVenda('jogador6')">+</button>
    <label class="goleiroHandebolText label_escolher_jogador" >Goleiro</label>
    <label class="posicao1HandebolText label_escolher_jogador">Posição 1</label>
    <label class="posicao2HandebolText label_escolher_jogador">Posição 2</label>
    <label class="posicao3HandebolText label_escolher_jogador">Posição 3</label>
    <label class="posicao4HandebolText label_escolher_jogador">Posição 4</label>
    <label class="posicao5HandebolText label_escolher_jogador">Posição 5</label>
    <label class="posicao6HandebolText label_escolher_jogador">Posição 6</label>
</div>
</div>`)

HTMLs.set("bloco_escolhe_jogador_conteudo", `
<div class="player">
<img src="FOTOJOGADOR" class="foto_jogador_escolher">
    <div style="display:flex; flex-direction: column; width: 100%;">
        <div style="display: flex; flex-direction: column; margin-left: 20px; margin-bottom: 10px;">
            <p style="margin: 0; font-family: 'Open Sans', sans-serif; color: #0F3B5E;" class="nome_jogador_escolher">NOMEJOGADOR</p>
            <p style="margin: 0; font-size: 10px;  color: #0F3B5E" class="equipe_jogador_escolher">EQUIPEJOGADOR</p>
        </div>
        <div style="display: flex; flex-direction: row; justify-content: space-between; width: 100%">
            <div style="display: flex; flex-direction: row; margin-left: 20px;">
                <div style="display: flex; flex-direction: column; text-align: center; margin-right: 5px;">
                    <p style="margin: 0; font-size: 11px; color: #0F3B5E; font-family: 'Open Sans', sans-serif;">última</p>
                    <p style="margin: 0; color: #FBB834" class="pontos_jogador">ULTIMOSPONTOSJOGADOR</p>
                </div>
                <div style="display: flex; flex-direction: column; text-align: center;">
                    <p style="margin: 0; font-size: 11px; color: #0F3B5E; font-family: 'Open Sans', sans-serif;">média</p>
                    <p style="margin: 0; color: #FBB834" class="pontos_jogador">MEDIAPONTOSJOGADOR</p>
                </div>
            </div>
            <button onclick="escolher_jogador('IDPOSICAO', 'FOTOJOGADOR', 'IDJOGADOR')" class="btn_escolher_jogador" style="ESTILOBTNESCOLHERJOGADOR" disabled>Selecionar</button>
        </div>
    </div>
</div>`)

HTMLs.set("bloco_escolhe_jogador", `
<div class="popUp" id="bloco_escolhe_jogador" style="opacity: 0%">
<i class="fa fa-arrow-left simbolo icon3" id="btn_voltar_escolhe_jogador" onclick="fechar_escolhe_jogador()"></i>
<div class="players" id="bloco_mostra_jogadores" style="opacity: 0%"></div>
</div>`)


var escalacoes = new Map

var esporteAtual = ""

HTMLs.set("HTML_bloco_escalacao_futsal_masculino_btns_de_escalacao", `goleiro, jogador1, jogador2, jogador3, jogador4`)
HTMLs.set("HTML_bloco_escalacao_futsal_feminino_btns_de_escalacao", `goleiro, jogador1, jogador2, jogador3, jogador4`)
HTMLs.set("HTML_bloco_escalacao_basquete_btns_de_escalacao", `jogador1, jogador2, jogador3, jogador4, jogador5`)
HTMLs.set("HTML_bloco_escalacao_handebol_btns_de_escalacao", `goleiro, jogador1, jogador2, jogador3, jogador4, jogador5, jogador6`)

carregarEscalacaoDoBancoDados()

var dadosJogadoresDoEsporteAtual
var proibido_voltar = false
//variaveis escalacao

const sleep = ms => new Promise(r => setTimeout(r, ms))

async function escalacao(esporte) {
    esporteAtual = esporte
    
    let escalao_atual_nome = "escalacao_" + esporte
    let escalao_atual = escalacoes.get(escalao_atual_nome)

    HTML_escalacao = HTMLs.get("HTML_bloco_escalacao_" + esporte)
    HTML_escalacao = HTML_escalacao.replace("PONTUACAONOESPORTEATUAL", escalacoes.get(escalao_atual_nome)["pontos"])
    
    await sleep(150)
    blocoEscolherEsporte.css("opacity", "0%")
    await sleep(100)
    blocoEscolherEsporte.html("")

    blocoEscalacao.css("opacity", "0%")
    blocoEscalacao.append(HTML_escalacao)
    blocoEscalacao.css("opacity", "100%")
    
    carregarJogadoresDoBD()
    carregarEscalacaoNoHTML(escalao_atual)

    if (mercado_aberto[esporteAtual] == "False") {
        $("#mercado_fechado").html("MERCADO FECHADO")
        $(".escolher_jogador").prop("disabled", true)

        $(".container_pontos_e_salvar").css("flex-direction", "column")
        $(".container_pontos_e_salvar").css("justify-content", "center")
        $("#btn_salvar").css("opacity", "0%")

        $(".escolher_jogador").css("opacity", "70%")
        $(".label_escolher_jogador").css("opacity", "70%")
        $("#quadra").css("opacity", "70%")
        $(".escolher_jogador").css("opacity", "70%")
        $(".pontos_escalacao").css("opacity", "70%")
        $(".esc_title2").css("opacity", "70%")

    } else {
        $("#mercado_fechado").remove()
        $(".container_pontos_e_salvar").css("justify-content", "space-evenly")
        $(".container_pontos_e_salvar").css("align-items", "stretch")
        $(".container_pontos_e_salvar").css("flex-direction", "row")
        $("#btn_salvar").css("opacity", "100%")
        $(blocoEscalacao).css("opacity", "100%")
    }
}

function carregarEscalacaoDoBancoDados() {
    $(".btn_escolhe_esporte").prop("disabled", true)
    $.ajax({
        url: "/dados-do-banco/escalacao",
        type: "GET",
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        contentType: "application/json",
        success: function(data) {
            escalacoes.set("escalacao_basquete", data["basquete"])
            escalacoes.set("escalacao_handebol", data["handebol"])
            escalacoes.set("escalacao_futsal_feminino", data["futsal_feminino"])
            escalacoes.set("escalacao_futsal_masculino", data["futsal_masculino"])
            $(".btn_escolhe_esporte").prop("disabled", false)
            console.log("sucesso")
        },
        error: function(e) {
            console.log(e)
        }
    })
}

function carregarEscalacaoNoHTML(escalacao) {
    for (posicao in escalacao) {
        let id = posicao
        let imagemJogador = escalacao[posicao][1]
        colocaJogadorNoHTML(id, imagemJogador)
    }
    
}

async function voltar(blocoAtual, blocoDestino) {
    if (!proibido_voltar) {
        $("#" + blocoAtual).css("opacity", "0%")
        await sleep(100)
        $("#" + blocoAtual).html("")

        $("#" + blocoDestino).css("opacity", "0%")
        $("#" + blocoDestino).append(HTMLs.get("HTML_" + blocoDestino))
        $("#" + blocoDestino).css("opacity", "100%")
    }
}

function carregarJogadoresDoBD() {
    $(".btn_escolhe_jogador").prop("disabled", true)
    $.ajax({
        url: "/dados-do-banco/jogadores",
        type: "POST",
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        data: JSON.stringify({"esporte": esporteAtual}),
        contentType: "application/json",
        success: function(data) {
            console.log(data, "dados")
            dadosJogadoresDoEsporteAtual = data
            $(".btn_escolhe_jogador").prop("disabled", false)
        },
        error: function(e) {
            console.log(e)
        }
    })
}

async function colocaJogadoresNoHTML(idPosição, posicao) {
    let HTML_escolhe_jogador_conteudo = HTMLs.get("bloco_escolhe_jogador_conteudo")    

    let conteudo = ""
    let conteudoJogador
    let escalacaoAtual
    jogadores = dadosJogadoresDoEsporteAtual[posicao]

    for (const jogador in jogadores) {
        let imagem = jogadores[jogador]["foto_de_perfil"]
        let nome = jogadores[jogador]["nome"]
        let equipe = jogadores[jogador]["equipe"]
        let pontosUltimaPartida = jogadores[jogador]["pontos_ultima_partida"]
        let mediaPontos = jogadores[jogador]["media_pontos"]

        if (!pontosUltimaPartida) {
            pontosUltimaPartida = "*"
            mediaPontos = "*"
        }

        if (equipe == "asia") {
            equipe = "Ásia"
        } else if (equipe == "america") {
            equipe = "América"
        } else {
            equipe = "África"
        }

        conteudoJogador = HTML_escolhe_jogador_conteudo.replaceAll("IDJOGADOR", jogador).replaceAll("FOTOJOGADOR", imagem).replaceAll("NOMEJOGADOR", nome).replaceAll("EQUIPEJOGADOR", equipe).replaceAll("ULTIMOSPONTOSJOGADOR", pontosUltimaPartida).replaceAll("MEDIAPONTOSJOGADOR", mediaPontos).replaceAll("IDPOSICAO", idPosição)
        escalacaoAtual = escalacoes.get(`escalacao_${esporteAtual}`)
        
        let jogadorEstaNaEscalacao = false
        for (posicao in escalacaoAtual) {
            if (escalacaoAtual[posicao] && posicao != "pontos") {
                if (escalacaoAtual[posicao][0].includes(jogador)) {
                    jogadorEstaNaEscalacao = true
                }
            }
        }

        if (jogadorEstaNaEscalacao) {
            conteudoJogador = conteudoJogador.replace("Selecionar", "Selecionado")
            conteudoJogador = conteudoJogador.replace("ESTILOBTNESCOLHERJOGADOR", "background-color: #c79229;")
        } else {
            conteudoJogador = conteudoJogador.replace("disabled", "")
            conteudoJogador = conteudoJogador.replace("ESTILOBTNESCOLHERJOGADOR", "")
        }
        
        conteudo += conteudoJogador
    }
    $("#bloco_mostra_jogadores").append(conteudo)
    await sleep(1)
    $(blocoEscolheJogador).css("opacity", "100%")
    $("#bloco_mostra_jogadores").css("opacity", "100%")

}

function verJogadoresaVenda(idPosição) {
    let posicao = idPosição == "goleiro" ? "gol":"ataque"

    blocoEscalacao.append(HTMLs.get('bloco_escolhe_jogador'))

    colocaJogadoresNoHTML(idPosição, posicao)
}

function colocaJogadorNoHTML(idPosição, imagemJogador) {
    let idElemento = "#"+idPosição
    let dadosBackgroundImage = "url(" + imagemJogador + ")"
    $(idElemento).html("")
    $(idElemento).css("background-image", dadosBackgroundImage)
}

function escolher_jogador(idPosição, imagemJogador, idJogador) {
    colocaJogadorNoHTML(idPosição, imagemJogador)

    dadosJaSalvos = inpFormulario.val()
    if (dadosJaSalvos) {
        dadosSalvarAtualizados = dadosJaSalvos + ';' + idJogador + ',' + idPosição
    } else {
        dadosSalvarAtualizados = idJogador + ',' + idPosição
    }
    
    inpFormulario.val(dadosSalvarAtualizados)

    let chave = "escalacao_" + esporteAtual

    console.log(escalacoes.get(chave))
    
    conteudo_map_na_chave_modificar = escalacoes.get(chave)
    conteudo_map_na_chave_modificar[idPosição] = [idJogador, imagemJogador]
    escalacoes.set(chave, conteudo_map_na_chave_modificar)
    
    console.log(escalacoes.get(chave)[idPosição])

    fechar_escolhe_jogador()
}

async function fechar_escolhe_jogador() {
    $("#bloco_escolhe_jogador").css("opacity", "0%")
    await sleep(1000)
    $("#bloco_escolhe_jogador").remove("")
}

function submit() {
    form.trigger("submit")
}

form.on("submit", async function salvar_escolhas(event) {
    event.preventDefault()
    dados = {0: inpFormulario.val(), 1: esporteAtual}
    if (inpFormulario.val()) {
        inpFormulario.val("")
        //let ajax1Rodou = false
        //let ajax2Rodou = false

        proibido_voltar = true
        $.ajax({
            url: "/",
            type: "POST",
            data: JSON.stringify(dados),
            contentType: "application/json",
            success: function(response) {
                //ajax1Rodou = true
                proibido_voltar = false
                console.log(response)
            },
            error: function(e) {
                window.location.reload()
                console.log(e)
            }
        })
        //$.ajax({
        //    url: `/dados-do-banco/escalacao/${esporteAtual}`,
        //    type: "get",
        //    headers: {
        //        'X-Requested-With': 'XMLHttpRequest'
        //    },
        //    success: function(data) {
        //        let key = "escalacao_"+esporteAtual
        //        escalacoes.set(key, data)
        //        ajax2Rodou = true
        //        console.log("escalacao atualizada")
        //    },
        //    error: function(e) {
        //        window.location.reload()
        //        console.log(e)
        //    }
        //})
//
        //while (proibido_voltar) {
        //    if (ajax1Rodou && ajax2Rodou) {
        //        proibido_voltar = false
        //        console.log("liberou")
        //    }
        //    await sleep(50)
        //}
    }
    //salvar todos os dados das escolhas do usuario em um form secreto e dar submit no mesmo após o salvamento das escolhas pelo usuario
})