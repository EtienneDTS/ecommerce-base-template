var products = document.querySelectorAll(".product");
var addToCartBtns = document.querySelectorAll(".add-to-cart");

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
    addToCartBtns[i].addEventListener("click", function(event) {
        console.log("cliqué")
        event.preventDefault();
      });
}



