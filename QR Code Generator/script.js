let textUrl = document.querySelector("#text-url");
let imageBox = document.querySelector(".img-box");
let image = document.querySelector("#image");
let btn = document.querySelector("#btn");

function qrCodeGenerate() {
    if (textUrl.value.length > 0) {
        let url = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${textUrl.value}`;
        image.src = url;
        imageBox.classList.add("new-box");
        image.classList.add("new-image"); z
    }
    else {
        textUrl.classList.add("error");
        setTimeout(() => {
            textUrl.classList.remove("error");
        }, 1000)
    }
}

btn.addEventListener("click", () => {
    qrCodeGenerate();
})