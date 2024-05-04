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

    setTimeout(loop, 0);
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
  // botão de registrar-se foi clicado?
  goToRegister.addEventListener("click",function (){
    window.location.href = '/'
  })
