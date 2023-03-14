// $('#add-to-cart-form').on('submit', function(event) {
//     event.preventDefault();
//     var form = $(this);
//     var url = form.attr('action');
//     var data = form.serialize();
//     $.ajax({
//         url: url,
//         type: 'POST',
//         data: data,
//         success: function(response) {
//             if (response.success) {
                
//             }
//         }
//     });
// });

var flavor_selector = document.getElementById("flavor-select");
var option_buttons = document.querySelectorAll('.option-for-option button');
console.log(option_buttons)
var hiddenInput = document.querySelector("#selected-option");
hiddenInput.value = default_selected_option
console.log(hiddenInput.value)

function redirectToVariantUrl(url) {
  window.location.href = url;
}

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
    });
  }



flavor_selector.addEventListener("change", ()=>{
    var flavor_selector_value = flavor_selector.value
    $.post(get_variant_view_url, {
      flavor: flavor_selector_value,
      csrfmiddlewaretoken : csrfToken,
    }, function(data) {
      var variant_slug = variant_url.replace("", data.url);
      console.log(new_url)
      redirectToVariantUrl(new_url);
    });
  });



