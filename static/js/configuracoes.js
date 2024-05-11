const button = document.getElementById("btn_submit");
const blurr = document.getElementById("blur");
const inputs = document.getElementsByTagName("input");
const popUp = document.getElementById("popUp");
const form = document.getElementById("form");

button.addEventListener("click", () => {
    blurr.style.filter = "blur(10px)";
    popUp.style.transform = "translate(-50%, -50%) scale(1)"
    popUp.style.visibility = "visible"
})
form.getElementsByTagName("i")[0].addEventListener("click", () => {
    window.location.href = "/"
})
popUp.getElementsByTagName("i")[0].addEventListener("click",()=>{
    blurr.style.filter = "blur(0px)";
    popUp.style.transform = "translate(-50%, 0) scale(0)"
    popUp.style.visibility = "hidden"
})
