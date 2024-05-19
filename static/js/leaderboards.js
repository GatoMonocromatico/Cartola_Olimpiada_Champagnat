const tabs = document.querySelectorAll(".tab_btn");
const all_content = document.querySelectorAll(".content");
const icon1 = document.querySelector("#icon1");
const icon2 = document.querySelector("#icon2");

let target = "times"

const africaBar = document.querySelector(".africaBar");
const asiaBar = document.querySelector(".asiaBar");
const americaBar = document.querySelector(".americaBar");

const heightCalculous = () =>{
    let somaPontos = africaPoints + asiaPoints + americaPoints;

    let africaHeight = 40 + 250 *(africaPoints / somaPontos) + "px";
    let asiaHeight = 40 + 250 *(asiaPoints / somaPontos) + "px";
    let americaHeight = 40 + 250 *(americaPoints / somaPontos) + "px";
    africaBar.style.height = africaHeight;
    asiaBar.style.height = asiaHeight;
    americaBar.style.height = americaHeight;
}

heightCalculous();

tabs.forEach((tab,index)=>{
    tab.addEventListener("click",(e)=>{
        tabs.forEach(tab=>{
            tab.classList.remove("active")
        })
        tab.classList.add("active");
        var line = document.querySelector(".line");
        line.style.left = e.target.offsetLeft + "px";
        line.style.width = e.target.offsetWidth + "px";
        if (index == 0) {
            target = "times"
        } else {
            target = "cartoleiros"
        }
        
        all_content.forEach(content=>{
            content.classList.remove("active")
        })
        all_content[index].classList.add("active")
    })
})

icon1.addEventListener("click",()=>{
    all_content[0].classList.remove("active")
    all_content[1].classList.add("active")
    target = "cartoleiros"
})
icon2.addEventListener("click",()=>{
    all_content[1].classList.remove("active")
    all_content[0].classList.add("active")
    target = "times"
})
const loop = () => {
    let line = document.querySelector(".line");

    if (target == "times") {
        line.style.left = tabs[0].offsetLeft + "px";
        line.style.width = tabs[0].offsetWidth + "px";
    }else{
        line.style.left = tabs[1].offsetLeft + "px";
        line.style.width = tabs[1].offsetWidth + "px";}
}

window.onresize = loop

document.addEventListener("DOMContentLoaded", loop())
