
var flavor_selector = document.getElementById("flavor-select");
var option_buttons = document.querySelectorAll('.option-for-option button');
console.log(option_buttons)
var hiddenInput = document.querySelector("#selected-option");
hiddenInput.value = default_selected_option
console.log(hiddenInput.value)


for (var i = 0; i < option_buttons.length; i++) {
    option_buttons[i].addEventListener('click', function(event) {
      // Désélectionne tous les boutons dans le même groupe que le bouton cliqué
      var group = this.closest('.option-buttons');
      group.querySelectorAll('.btn').forEach(function(button) {
        button.classList.remove('active');
      });
      
      // Sélectionne le bouton cliqué
      event.target.classList.add('active');
      
      // Met à jour la valeur du champ caché
      hiddenInput.value = event.target.dataset.value;
      
      console.log(hiddenInput.value)
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
          document.querySelector('img').src = data.product_variant.image;
    
          // Met à jour le prix du produit
          document.querySelector('span').textContent = data.product_variant.price + " €";
        }
      });
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



