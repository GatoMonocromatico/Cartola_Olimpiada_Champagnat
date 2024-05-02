const bloco_login = $("#bloco_login")
const inpLoginUsuario = $("#inp_usuario_login")
const placeholderLoginUsuario = $("#placeholder_usuario_login")
const inpLoginSenha = $("#inp_senha_login")
const placeholderLoginSenha = $("#placeholder_senha_login")
const btn_login = $("#botao_login")
//variaveis login
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

inpLoginUsuario.on("focus", function () {
    placeholderLoginUsuario.css("opacity", "0")
})

inpLoginSenha.on("focus", function () {
    placeholderLoginSenha.css("opacity", "0")
})

btn_login.on("click", function () {
    bloco_login.css("opacity", "0")
    blocoEscolherEsporte.css("opacity", "100%")
})
//funções login

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