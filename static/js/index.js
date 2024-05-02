const blocoEscolherEsporte = $("#bloco_escolha_do_esporte")
const btnEscolheFutsalMasc = $("#btn_escolhe_futsal_masc")
const btnEscolheFutsalFem = $("#btn_escolhe_futsal_fem")
const btnEscolheBasquete = $("#btn_escolhe_basquete")
const btnEscolheHandebol = $("#btn_escolhe_handebol")
const btnEscolheEsporteQualquer = $(".btn_escolhe_esporte")
//variaveis escolher esporte
const blocoEscalacao = $("#bloco_escalacao")
const btnEscolheJogador = $(".btn_escolhe_jogador")
const blocoEscolheJogador = $("#bloco_escolhe_jogador")
//variaveis escalacao


btnEscolheEsporteQualquer.on("click", function() {
    blocoEscolherEsporte.css("opacity", "0")
    blocoEscalacao.css ("opacity", "100%")
})

btnEscolheFutsalMasc.on("click", function () {
    let HTMLescalacaoFutsalMasc = ""

    blocoEscalacao.append(HTMLescalacaoFutsalMasc)
})

btnEscolheFutsalFem.on("click", function () {
//    bloco_escolher_esporte.css("opacity", "0")
})

btnEscolheBasquete.on("click", function () {
//    bloco_escolher_esporte.css("opacity", "0")
})

btnEscolheHandebol.on("click", function () {
//    bloco_escolher_esporte.css("opacity", "0")
})

btnEscolheJogador.on("click", function() {

})
//funções escolher esporte