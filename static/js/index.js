const body = "body"

const blocoEscolherEsporte = $("#bloco_escolha_do_esporte")
const btnEscolheFutsalMasc = "#btn_escolhe_futsal_masc"
const btnEscolheFutsalFem = "#btn_escolhe_futsal_fem"
const btnEscolheBasquete = "#btn_escolhe_basquete"
const btnEscolheHandebol = "#btn_escolhe_handebol"
const btnEscolheEsporteQualquer = ".btn_escolhe_esporte"

var HTMLs = new Map
HTMLs.set("HTML_bloco_escolha_do_esporte", `
<button id="btn_escolhe_futsal_masc" class="btn_escolhe_esporte" onclick="escalacao('futsal_masculino')">Futsal Masculino</button>
<button id="btn_escolhe_futsal_fem" class="btn_escolhe_esporte" onclick="escalacao('futsal_feminino')">Futsal Feminino</button>
<button id="btn_escolhe_basquete" class="btn_escolhe_esporte" onclick="escalacao('basquete')">Basquete</button>
<button id="btn_escolhe_handebol" class="btn_escolhe_esporte" onclick="escalacao('handebol')">Handebol</button>
`)

//variaveis escolher esporte
const blocoEscalacao = $("#bloco_escalacao")
const btnEscolheJogador = ".btn_escolhe_jogador"
const blocoEscolheJogador = "#bloco_escolhe_jogador"
const btnVoltar = "#btn_voltar_escalacao"

HTMLs.set("HTML_bloco_escalacao_futsal_masculino", `
<span class="simbolo" id="btn_voltar_escalacao" onclick="voltar('bloco_escalacao', 'bloco_escolha_do_esporte')"><</span>
<button class="btn_escolhe_jogador simbolo" id="goleiro">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador1">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador2">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador3">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador4">+</button>
<img src="static/quadra_futsal.png" id="quadra">

<div id="bloco_escolhe_jogador">
    <div id="jogador_1">
        <img src="">
        <label>jogador genérico</label>
        <label>equipe 1</label>
        <button>Comprar</button>
</div>`)
HTMLs.set("HTML_bloco_escalacao_futsal_feminino", `
<span class="simbolo" id="btn_voltar_escalacao" onclick="voltar('bloco_escalacao', 'bloco_escolha_do_esporte')"><</span>
<button class="btn_escolhe_jogador simbolo" id="goleiro">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador1">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador2">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador3">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador4">+</button>
<img src="static/quadra_futsal.png" id="quadra">

<div id="bloco_escolhe_jogador">
    <div id="jogador_1">
        <img src="">
        <label>jogador genérico</label>
        <label>equipe 1</label>
        <button>Comprar</button>
</div>`)
HTMLs.set("HTML_bloco_escalacao_basquete", `
<span class="simbolo" id="btn_voltar_escalacao" onclick="voltar('bloco_escalacao', 'bloco_escolha_do_esporte')"><</span>
<button class="btn_escolhe_jogador simbolo" id="jogador1">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador2">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador3">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador4">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador5">+</button>
<img src="static/quadra_basquete.png" id="quadra">

<div id="bloco_escolhe_jogador">
    <div id="jogador_1">
        <img src="">
        <label>jogador genérico</label>
        <label>equipe 1</label>
        <button>Comprar</button>
</div>`)
HTMLs.set("HTML_bloco_escalacao_handebol", `
<span class="simbolo" id="btn_voltar_escalacao" onclick="voltar('bloco_escalacao', 'bloco_escolha_do_esporte')"><</span>
<button class="btn_escolhe_jogador simbolo" id="goleiro">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador1">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador2">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador3">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador4">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador5">+</button>
<button class="btn_escolhe_jogador simbolo" id="jogador6">+</button>
<img src="static/quadra_handebol.png" id="quadra">

<div id="bloco_escolhe_jogador">
    <div id="jogador_1">
        <img src="">
        <label>jogador genérico</label>
        <label>equipe 1</label>
        <button>Comprar</button>
</div>`)
//variaveis escalacao

function escalacao(esporte) {
    HTML_escalacao = HTMLs.get("HTML_bloco_escalacao_"+esporte)

    blocoEscolherEsporte.html("")
    blocoEscalacao.append(HTML_escalacao)
}


function voltar(blocoAtual, blocoDestino) {
    $("#" + blocoAtual).html("")
    $("#" + blocoDestino).append(HTMLs.get("HTML_" + blocoDestino))
}

function comprar_jogador(posição, id_posição)
