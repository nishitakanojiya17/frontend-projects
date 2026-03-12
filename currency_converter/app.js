let dropdowns = document.querySelectorAll(".select-container select");
let btn = document.querySelector("button");
let from = document.querySelector(".from select")
let to = document.querySelector(".to select")
let msg = document.querySelector(".msg")
for (let select of dropdowns) {
    for (let curcode in currencyToCountry) {
        let newOption = document.createElement("option");
        newOption.innerText = curcode;
        newOption.value = curcode;
        if (select.name == "from" && curcode == "USD") {
            newOption.selected = "selected";
        }
        else if (select.name == "to" && curcode == "INR") {
            newOption.selected = "selected";
        }
        select.append(newOption);
    }

    select.addEventListener("change", (evt) => {
        console.log(evt.target.value);
        let img = select.parentElement.querySelector("img");
        img.src = `https://flagsapi.com/${currencyToCountry[evt.target.value]}/flat/64.png`
    })
}
async function exchangeAmount(amountValue) {
    let url = `https://api.frankfurter.app/latest?amount=1&from=${from.value}&to=${to.value}`;
    let response = await fetch(url)
    let data = await response.json();
    console.log(data.rates[to.value]);
    let exvalue = data.rates[to.value];
    let res = amountValue * exvalue;
    console.log(res);
    msg.innerText = `${amountValue}${from.value} = ${res}${to.value}`
}
btn.addEventListener("click", (evt) => {
    evt.preventDefault();
    let amount = document.querySelector(".amount input");
    let amountValue = amount.value;
    if (amountValue == "" || amountValue < 1) {
        amount.value = "1";
        amountValue = "1";
    }
    console.log(amountValue)
    exchangeAmount(amountValue);
})
window.addEventListener("load", (evt) => {
    evt.preventDefault();
    let amount = document.querySelector(".amount input");
    let amountValue = amount.value;
    if (amountValue == "" || amountValue < 1) {
        amount.value = "1";
        amountValue = "1";
    }
    console.log(amountValue)
    exchangeAmount(amountValue);
})