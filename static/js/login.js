const bloco_login = $("#bloco_login")
const inpLoginUsuario = $("#inp_usuario_login")
const placeholderLoginUsuario = $("#placeholder_usuario_login")
const inpLoginSenha = $("#inp_senha_login")
const placeholderLoginSenha = $("#placeholder_senha_login")
const btn_login = $("#botao_login")
const btnTrocaSigninSignup = $("#trocar_signin_signup")
const bloco_login_inputs = $("#bloco_login_inputs")
//variaveis login

inpLoginUsuario.on("focus", function () {
    placeholderLoginUsuario.css("opacity", "0")
})

inpLoginSenha.on("focus", function () {
    placeholderLoginSenha.css("opacity", "0")
})

btnTrocaSigninSignup.on("click", function() {
    let novoAttr = ""
    if (btn_login.attr("name") == "signin") {
        novoAttr = "signup"
        bloco_login_inputs.append('<div class="bloco_filho_bloco_login" id="bloco_login_nome"><div class="container">●</div><span class="placeholder_login" id="placeholder_nome_login">nome</span><input type="text" id="inp_nome_login" class="inp_login" name="nome" required></div>')
        btn_login.css("margin-top", "calc(10vh - 50px)")
    }
    else {
        novoAttr = "signin"
        $("#bloco_login_nome").remove()
        btn_login.css("margin-top", "15vh")
    }

    btn_login.attr("name", novoAttr)
})

//funções login