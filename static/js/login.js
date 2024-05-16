// pegando os elementos
const body = document.getElementById('body');
const form = document.getElementById('form');
const inputColunm = document.getElementById('input-colunm');
const usuarioESenha = document.getElementById('usuario_e_senha');

const detail1 = document.getElementById('detail1');
const detail2 = document.getElementById('detail2');
const detail3 = document.getElementById('detail3');
const detail4 = document.getElementById('detail4');

const matriculaInput = document.getElementById('matrícula');
const passwordInput = document.getElementById('password');
const eye = document.getElementById('eye-icon');

const button = document.getElementById('button');
const goToRegister = document.getElementById('goToRegister');

const button_jq = $("#button")
const btnTrocaSigninSignup = $("#trocar_signin_signup")
const bloco_login_inputs = $("#bloco_login_inputs")
const introdutorBtnTrocaSigninSignup = $("#introdutor_trocar_signin_signup")

const inpLoginNomeAparente = $("#inp_nome_login_aparente")
const inpLoginNomeForm = $("#inp_nome_login_form")

const inpLoginEquipeAfricaForm = $("#radio_africa_form")
const inpLoginEquipeAmericaForm = $("#radio_america_form")
const inpLoginEquipeAsiaForm = $("#radio_asia_form")

// função de posicionamento dinâmico dos detalhes
function placingElements() {

  // pegando as larguras e alturas  
  var formWidth = form.offsetWidth
  var formHeight = form.offsetHeight 
  var bodyWidth = body.offsetWidth
  var passwordInputWidth = passwordInput.offsetWidth
  var passwordInputHeight = passwordInput.offsetHeight

  // calculando os valores do posicionamento animado dos elementos
  var iconMarginTopValue = - (((passwordInputHeight - 16) / 2 + 16) + 15)
  var iconRigthValue = (bodyWidth - passwordInputWidth) / 2 + 15
  var detail1RightValue = ((bodyWidth - formWidth) / 2) - 16
  var detail2TopValue = 100 + formHeight
  var detail2LeftValue = (bodyWidth - formWidth) / 2 - 27
  var detail3rightValue = ((bodyWidth - formWidth) / 2) - 32.5
  var detail4LeftValue = ((bodyWidth - formWidth) / 2) - 32.5

  //setando a posição dos elementos
  detail1.style.right = detail1RightValue + 'px';
  detail2.style.top = detail2TopValue + 'px';
  detail2.style.left = detail2LeftValue + 'px';
  detail3.style.right =  detail3rightValue+ 'px';
  detail4.style.left = detail4LeftValue + 'px';

  eye.style.right = iconRigthValue + 'px';
  eye.style.marginTop = iconMarginTopValue + 'px';
  
  
  console.log("rodou")
}

//eventListeners:

document.addEventListener("DOMContentLoaded", placingElements())
window.onresize = placingElements

  //o botão do olho foi clicado?
function eyeClicado() {
  if (eye.className == 'fas fa-eye') {
    passwordInput.type = 'password';
    eye.className = 'fas fa-eye-slash';
  }
  else{
    passwordInput.type = "text"
    eye.className = 'fas fa-eye';
  }
};
//animação do botão do olho
passwordInput.addEventListener('mousedown', function() {
  eye.style.transform = "translateY(6px) translateX(-6px)";
})
passwordInput.addEventListener('mouseup', function() {
  eye.style.transform = "translateY(0px) translateX(0px)";
})
// botão de registrar foi clicado?
button.addEventListener('click', function() {
  if ( matriculaInput.value == "" || passwordInput.value == "") {
    matriculaInput.style.borderColor = "#0F3B5E";
    passwordInput.style.borderColor = "#0F3B5E";
    if (matriculaInput.value == "") {
      matriculaInput.style.borderColor = "#ff0000";
    }
    if (passwordInput.value == "") {
      passwordInput.style.borderColor = "#ff0000";
    }
  }else{
    matriculaInput.style.borderColor = "#0F3B5E";
    passwordInput.style.borderColor = "#0F3B5E";
  }
})

btnTrocaSigninSignup.on("click", function() {
  let novoAttr = ""
  if (button_jq.attr("name") == "signin") {
      novoAttr = "signup"
      bloco_login_inputs.append('<input type="text" placeholder="Nome" class="input" id="inp_nome_login_aparente"/>')
      bloco_login_inputs.append('<div id="radios_container"><div class="div_radio"><input type="radio" name="equipeAparente" id="radio_africa" value="africa" checked><label for="radio_africa">Equipe Africa</label></div><div class="div_radio"><input type="radio" name="equipeAparente" id="radio_america" value="america"><label for="radio_america">Equipe América</label></div><div class="div_radio"><input type="radio" name="equipeAparente" id="radio_asia" value="asia"><label for="radio_asia">Equipe Ásia</label></div></div>')
      button_jq.css("margin-top", "20px")
      introdutorBtnTrocaSigninSignup.html("Já possui uma conta?")
      btnTrocaSigninSignup.html("Sign in")
      button_jq.html('<b class="sign-up-text">Registrar</b>')
  }
  else {
      novoAttr = "signin"
      $("#inp_nome_login_aparente").remove()
      $("#radios_container").remove()
      button_jq.css("margin-top", "70px")
      introdutorBtnTrocaSigninSignup.html("Não possui uma conta?")
      btnTrocaSigninSignup.html("Registrar")
      button_jq.html('<b class="sign-up-text">Sign in</b>')
      inpLoginNomeForm.val("")
  }

  button_jq.attr("name", novoAttr)
})

$("#myform").on("submit", function(event) {
  let acao, usuario, senha, nome, equipe
  event.preventDefault();

  if (button_jq.attr("name") == "signup") {
    inpLoginNomeForm.val($("#inp_nome_login_aparente").val())

    if ($("#radio_africa").is(":checked")) {
      inpLoginEquipeAfricaForm.prop("checked", true)
      equipe = "africa"
    }
    else if ($("#radio_america").is(":checked")) {
      inpLoginEquipeAmericaForm.prop("checked", true)
      equipe = "america"
    }
    else {
      inpLoginEquipeAsiaForm.prop("checked", true)
      equipe = "asia"
    }
  }
  else {
    inpLoginNomeForm.val("None")
  }
  acao = button_jq.attr("name")
  usuario = $("#matrícula").val()
  senha = $("#password").val()
  nome = $("#inp_nome_login_form").val()

  dados = {
    [acao]: true,
    "usuario" : usuario,
    "senha": senha,
    "nome": nome,
    "equipe": equipe
  }

  console.log(dados)

  $.ajax({
    url: "/login",
    type: "POST",
    data: dados,
    contentType: "application/x-www-form-urlencoded",
    success: function(data) {
        status_login = data["login"]
        if (status_login == 20000) {
          $("#matrícula").val("None")
          $("#password").val("None")
          $("#inp_nome_login_form").val("None")
          
          window.location.replace("/")
        }
        else {
          let erro
          if (status_login == 40001) {
            erro = "Você já possui uma conta"
          }else if (status_login == 40002) {
            erro = "Usuário inexistente"
          }else if (status_login == 40010) {
            erro = "Número de matrícula inválido"
          }else if (status_login == 40020) {
            erro = "Senha inválida"
          }else if (status_login == 40030) {
            erro = "Nome inválido"
          }
          $("#erro").html(erro)
        }
    },
    error: function(e) {
        console.log(e)
    }
  })}
)
