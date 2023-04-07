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

