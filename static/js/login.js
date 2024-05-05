// pegando os elementos
const body = document.getElementById('body');
const form = document.getElementById('form');
const inputColunm = document.getElementById('input-colunm');

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

// função de loop
function loop() {
    // pegando as larguras e alturas  
    var formWidth = form.offsetWidth
    var formHeight = form.offsetHeight 
    var bodyWidth = body.offsetWidth
    var passwordInputWidth = passwordInput.offsetWidth
    var inputColunmHeight = inputColunm.offsetHeight

    // calculando os valores do posicionamento animado dos elementos
    var iconTopValue = 245.5 + ((formHeight - inputColunmHeight) / 2)
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
    eye.style.top = iconTopValue + 'px';
    console.log("rodou")

    setTimeout(loop, 50);
  }
  
// Inicia o loop
loop();

//eventListeners:
  //o botão do olho foi clicado?
  eye.addEventListener('click', function() {
    if (eye.className == 'fas fa-eye') {
      passwordInput.type = 'password';
      eye.className = 'fas fa-eye-slash';
    }
    else{
      passwordInput.type = "text"
      eye.className = 'fas fa-eye';
    }
  });
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
      button_jq.css("margin-top", "20px")
      introdutorBtnTrocaSigninSignup.html("Já possui uma conta?")
      btnTrocaSigninSignup.html("Sign in")
      button_jq.html('<b class="sign-up-text">Registrar</b>')
  }
  else {
      novoAttr = "signin"
      $("#inp_nome_login_aparente").remove()
      button_jq.css("margin-top", "70px")
      introdutorBtnTrocaSigninSignup.html("Não possui uma conta?")
      btnTrocaSigninSignup.html("Registrar")
      button_jq.html('<b class="sign-up-text">Registrar</b>')
      button_jq.html('<b class="sign-up-text">Sign in</b>')
      inpLoginNomeForm.val("")
  }

  button_jq.attr("name", novoAttr)
})

$("body").on("keyup", function() {
  if (button_jq.attr("name") == "signup") {
    inpLoginNomeForm.val($("#inp_nome_login_aparente").val())
  }
  else {
    inpLoginNomeForm.val("None")
  }
})
