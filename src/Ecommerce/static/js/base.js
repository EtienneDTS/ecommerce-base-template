let dropdown_remove_btn
let badge = document.querySelector(".badge");
console.log(badge)
// Section get_cart_url

const trash_icon_url = document.querySelector("#get_trash_icon_url").getAttribute("url")
function get_cart_data() {
  fetch("/shop/get_cart_data")
    .then(response => response.json())
    .then(data => {
      console.log(data)
      var products = data.products;
      var totalQuantity = data.total_quantity;
      var totalPrice = data.total_ttc;
      var container = document.querySelector(".cart__container");
      badge.innerHTML = totalQuantity

      // Vider le contenu actuel du panier
      container.innerHTML = "";

      // Ajouter les produits renvoyés par l'API à la vue
      products.forEach(function(product) {
        var item = `
          <div class="cart__product">
            <a href="${product.url}">
              <div class="cart__image-container">
                <img src="${product.image}" alt="${product.name}" class="cart__image">
              </div>
            </a>
            <div class="cart__product-details">
              <a href="${product.url}">
                <h2 class="cart__product-title">${product.name} x ${product.quantity}</h2>
              </a>
              <div class="update_cart_product_quantity"> 
                <p class="cart__total-price">${product.price} €</p>
              </div>
            </div>
            <div class="cart__product-buttons">
              <div class="cart__button-remove" id="${product.id}">
                <div class="cart_product-buttons-icon">
                  <img src="${trash_icon_url}" alt="trash icon">
                </div>
              </div>
            </div>
          </div>
        `;
        container.insertAdjacentHTML("beforeend", item);
        console.log(totalQuantity)
        
      });

      // Mettre à jour les informations de résumé du panier
      document.querySelector(".cart__quantity-number").textContent = totalQuantity;
      document.querySelector(".cart__total-number").textContent = totalPrice + " €";
      dropdown_remove_btn = document.querySelectorAll(".cart__button-remove")
      dropdown_remove_btn.forEach(btn =>{
        const cartProductId = btn.getAttribute("id");
        btn.addEventListener("click", (event) => {
          console.log(btn)
          fetch(`/remove_dropdown/${cartProductId}/`)
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
            })
            .then(success => {
              get_cart_data();
          })
          .catch(error => console.error(error));
        });
      })
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener("DOMContentLoaded", function(event) {
  get_cart_data();
});
// End Section get_cart_url



// Section hamburgermenu
const hamburgerMenu = document.querySelector('.nav__hamburger-menu');
const toggleMenu = document.querySelector('.toggle-menu')

hamburgerMenu.addEventListener('click', function() {
  this.classList.toggle('active');
  toggleMenu.classList.toggle('active');
});
// End Section hamburgermenu


// Section cart_dopdown
const cart_icon = document.querySelector(".nav__cart-icon")
const cart_dropdown = document.querySelector(".cart_dropdown")
let hover_timer 
cart_icon.addEventListener("mouseenter", ()=>{
  clearTimeout(hover_timer);
  cart_dropdown.classList.add("show")
})

cart_icon.addEventListener("mouseleave", ()=>{
  hover_timer = setTimeout(() => {
    cart_dropdown.classList.remove('show');
  }, 600);
})
cart_dropdown.addEventListener("mouseover", ()=>{
  clearTimeout(hover_timer);
  cart_dropdown.classList.add("show")
})
cart_dropdown.addEventListener("mouseleave", ()=>{
  hover_timer = setTimeout(() => {
    cart_dropdown.classList.remove('show');
  }, 600);
})








// End Section cart_dopdown