
var flavor_selector = document.getElementById("flavor-select");
var option_buttons = document.querySelectorAll('.product-details__option-buttons button');
var hiddenInput = document.querySelector("#selected-option");
hiddenInput.value = default_selected_option




for (var i = 0; i < option_buttons.length; i++) {
    option_buttons[i].addEventListener('click', function(event) {
      // Désélectionne tous les boutons dans le même groupe que le bouton cliqué
      var group = this.closest('.product-details__option-buttons');
      group.querySelectorAll('.btn').forEach(function(button) {
        button.classList.remove('active');
      });
      
      // Sélectionne le bouton cliqué
      event.target.classList.add('active');
      
      // Met à jour la valeur du champ caché
      hiddenInput.value = event.target.dataset.value;

      $.ajax({
        url: update_variant_detail,
        type: "POST",
        data: {
          csrfmiddlewaretoken: csrfToken,
          flavor: flavor_selector.value,
          option: hiddenInput.value
        },
        success: function(data) {
          // Met à jour l'image du produit
          document.getElementById('product-details__main-image').src = data.image_url;
    
          // Met à jour le prix du produit
          document.getElementById('product-details__price-info').textContent = data.price + " €";
          document.getElementById("variant-slug-input").value = data.slug
        }
      })
    });
  }



flavor_selector.addEventListener("change", ()=>{
    var flavor_selector_value = flavor_selector.value
    $.post(get_variant_view_url, {
      flavor: flavor_selector_value,
      csrfmiddlewaretoken : csrfToken,
    }, function(data) {
      var new_url = window.location.origin + data.url;
      history.replaceState(null, null, new_url);
      window.location.reload();
    });
  });

var inputNumber = document.querySelector('input[name="quantity"]');
var incrementButton = document.querySelector('#increment');
var decrementButton = document.querySelector('#decrement');

incrementButton.addEventListener('click', function() {
  inputNumber.value = parseInt(inputNumber.value) + 1;
});

decrementButton.addEventListener('click', function() {
  if (inputNumber.value > 1) {
    inputNumber.value = parseInt(inputNumber.value) - 1;
  }
});

$(document).ready(function() {
  $('.product-details__add-to-cart button').click(function(e) {
      e.preventDefault();
      
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
              var badge = document.querySelector(".badge")
              
              var notification = document.querySelector(".notification");
              var btn = document.querySelector(".btn-primary");
              btn.classList.add("btn-loading")
              setTimeout(function(){
                notification.classList.add('show');
                btn.classList.remove("btn-loading");
                badge.innerHTML = data.new_cart_quantity;
              }, 500);
              setTimeout(function() {
                notification.classList.remove('show');
              }, 3000);
          },
      });
  });
});

