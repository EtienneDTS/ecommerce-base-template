document.addEventListener("DOMContentLoaded", function(event) {
    get_cart_data();
  });

var products = document.querySelectorAll(".product");
var addToCartBtns = document.querySelectorAll(".add-to-cart");
var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

for (let i = 0; i < products.length; i++) {

  products[i].addEventListener('mouseover', function(event) {
    var addToCartBtn = event.currentTarget.querySelector('.add-to-cart');
    addToCartBtn.classList.add('active');
  });
    
  products[i].addEventListener('mouseout', function(event) {
    var addToCartBtn = event.currentTarget.querySelector('.add-to-cart');
    addToCartBtn.classList.remove('active');
  });
}

for (let i=0; i<addToCartBtns.length; i++) {
    $(document).ready(function() {
    addToCartBtns[i].addEventListener("click", function(event) {
        event.preventDefault();
        var btn = addToCartBtns[i]
        var form = $(this).closest('form');
        var url = form.attr('action');
        var data = form.serialize();
            
        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            },
            success: function(data) {
                // Afficher un message de confirmation ou rediriger vers la page de panier
                var notification = document.querySelector(".notification");
                btn.classList.add("btn-loading");
                get_cart_data()
                setTimeout(function(){
                    btn.classList.remove("btn-loading");
                    notification.classList.add('show');
                    var badge = document.querySelector(".badge");
                    badge.innerHTML = data.new_cart_quantity;
                }, 500);
                setTimeout(function() {
                    notification.classList.remove('show');
                }, 3000);
            },
        });
    });
});
}

const rangeInput = document.querySelectorAll(".range_input input")
const priceInput = document.querySelectorAll(".price_input input")
const progress = document.querySelector(".progress") 
let priceGap = 0
rangeInput[0].value = priceInput[0].value  
rangeInput[1].value = priceInput[1].value 
let minVal = parseInt(priceInput[0].value);
let maxVal = parseInt(priceInput[1].value);
progress.style.left = (minVal / rangeInput[0].max) * 100 + "%";
progress.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
let max_variant_price = document.querySelector(".range_max").max


priceInput.forEach(input=>{
    input.addEventListener("input", e=>{
        let minVal = parseInt(priceInput[0].value),
        maxVal = parseInt(priceInput[1].value);
        if((maxVal - minVal >= priceGap) && maxVal <= max_variant_price){
            console.log("salut")
            rangeInput[0].value = minVal;
            rangeInput[1].value = maxVal;
            progress.style.left = (minVal / rangeInput[0].max) * 100 + "%";
            progress.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%"; 
        }
    })
})

rangeInput.forEach(input=>{
    input.addEventListener("input", e=>{
        let minVal = parseInt(rangeInput[0].value),
        maxVal = parseInt(rangeInput[1].value);
        if(maxVal - minVal < priceGap){
            if(e.target.className === "range_min") {
                rangeInput[0].value = maxVal - priceGap;
            }else{
                rangeInput[1].value = minVal - priceGap;
            }
        
        }else{
            priceInput[0].value = minVal
            priceInput[1].value = maxVal
            progress.style.left = (minVal / rangeInput[0].max) * 100 + "%";
            progress.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
        }
    })
})

const filterShow= document.querySelector(".show_filter")
const toolsContainer = document.querySelector(".sort_tools_container")

filterShow.addEventListener("click", ()=>{
    toolsContainer.classList.toggle("show")
})

let sort_by_close_btn = document.querySelector(".sort_by_filter")
let price_filter_close_btn = document.querySelector(".price_filter")
const sort_select = document.querySelector("#sort_select")
let form_btn = document.querySelector(".form_btn")
let input_min = document.querySelector(".input_min")
let input_max = document.querySelector(".input_max")
let range_max = document.querySelector(".range_max")

if (sort_by_close_btn) {
    sort_by_close_btn.addEventListener("click", (event)=>{
        event.preventDefault()
        sort_select.value = "none"
        form_btn.click()
    });
}

if (price_filter_close_btn) {
    price_filter_close_btn.addEventListener("click", ()=>{
        input_min.value = "0"
        input_max.value = range_max.max
        form_btn.click()
    });
}