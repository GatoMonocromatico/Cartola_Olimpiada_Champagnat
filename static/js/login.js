const bloco_login = $("#bloco_login")
const inpLoginUsuario = $("#inp_usuario_login")
const placeholderLoginUsuario = $("#placeholder_usuario_login")
const inpLoginSenha = $("#inp_senha_login")
const placeholderLoginSenha = $("#placeholder_senha_login")
const btn_login = $("#botao_login")
//variaveis login

inpLoginUsuario.on("focus", function () {
    placeholderLoginUsuario.css("opacity", "0")
})

inpLoginSenha.on("focus", function () {
    placeholderLoginSenha.css("opacity", "0")
})
//funções login