// pegando os botões
const futMascBut = document.getElementById("futMascBut");
const futFemBut = document.getElementById("futFemBut");
const handBut = document.getElementById("handBut");
const basketBut = document.getElementById("basketBut");
const container = document.getElementById("container");

//pegando os textos dos botões
const futMascText = document.getElementById("futMascText");
const futFemText = document.getElementById("futFemText");
const handText = document.getElementById("handText");
const basketText = document.getElementById("basketText");

//pegando os icones
const img1 = document.getElementById("futMascIcon");
const img2 = document.getElementById("futFemIcon");
const img3 = document.getElementById("handIcon");
const img4 = document.getElementById("baskIcon");

//funçõa de loop 
function loop(){
    //pegando o tamanho dos botões
    var but1Height = futMascBut.offsetHeight
    var but2Height = futFemBut.offsetHeight
    var but3Height = handBut.offsetHeight
    var but4Height = basketBut.offsetHeight

    //calculando o quanto de margin-rigth os icones devem ter
    var img1Right = futMascBut.offsetWidth - (50/100 * img1.offsetWidth)
    var img2Right = futFemBut.offsetWidth - (65/100 * img2.offsetWidth)
    var img3Right = handBut.offsetWidth - (50/100 * img3.offsetWidth)
    var img4Right = basketBut.offsetWidth - (110/100 * img4.offsetWidth)

    //alterando o tamanho dos icones conforme o necessário
    img1.style.height = 105/100 * but1Height + "px";
    img2.style.height = 115/100 * but2Height + "px";
    img3.style.height = 120/100 * but3Height + "px";
    img4.style.height = 137/100 * but4Height + "px";

    //alterando o margin-right dos icones conforme o necessário
    img1.style.marginRight = img1Right + "px";
    img2.style.marginRight = img2Right + "px";
    img3.style.marginRight = img3Right + "px";
    img4.style.marginRight = img4Right + "px";

    //alterando o margin-bottom dos icones conforme o necessário
    img1.style.marginBottom = 17 + "px";
    img2.style.marginBottom = 27 + "px";
    img3.style.marginBottom = 34 + "px";
    img4.style.marginBottom = 57 + "px";

    setTimeout(loop,1)
}
//botando o loop pra funcionar a cada 1 segundo
loop()

//funções de mouseenter e mouseleave dos botões para as animações
futMascBut.addEventListener("mouseenter", () => {
    img1.style.opacity = "100%";
    futMascBut.style.height = "25%";
    futMascText.style.color = "#FBB834";
    futMascText.style.fontSize = "18px";
})
futMascBut.addEventListener("mouseleave", () => {
    img1.style.opacity = "0%";
    futMascBut.style.height = "15%";
    futMascText.style.color = "#0F3B5E";
    futMascText.style.fontSize = "14px";
})
futFemBut.addEventListener("mouseenter", () => {
    img2.style.opacity = "100%";
    futFemBut.style.height = "25%";
    futFemText.style.color = "#FBB834";
    futFemText.style.fontSize = "18px";
})
futFemBut.addEventListener("mouseleave", () => {
    futFemBut.style.height = "15%";
    img2.style.opacity = "0%";
    futFemText.style.color = "#0F3B5E";
    futFemText.style.fontSize = "14px";
})
handBut.addEventListener("mouseenter", () => {
    img3.style.opacity = "100%";
    handBut.style.height = "25%";
    handText.style.color = "#FBB834";
    handText.style.fontSize = "18px";
})
handBut.addEventListener("mouseleave", () => {
    img3.style.opacity = "0%";
    handBut.style.height = "15%";
    handText.style.color = "#0F3B5E";
    handText.style.fontSize = "14px";
})
basketBut.addEventListener("mouseenter", () => {
    img4.style.opacity = "100%";
    basketBut.style.height = "25%";
    basketText.style.color = "#FBB834";
    basketText.style.fontSize = "18px";
})
basketBut.addEventListener("mouseleave", () => {
    img4.style.opacity = "0%";
    basketBut.style.height = "15%";
    basketText.style.color = "#0F3B5E";
    basketText.style.fontSize = "14px";
})
