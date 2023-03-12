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

function selectButton(button) {
    // Désélectionne tous les boutons dans le même groupe que le bouton cliqué
    var group = button.closest('.option-buttons');
    group.find('.btn').removeClass('active');
    
    // Sélectionne le bouton cliqué
    button.addClass('active');
    
    // Met à jour la valeur du champ caché
    var hiddenInput = group.find('input[type=hidden]');
    hiddenInput.val(button.data('value'));
    console.log(hiddenInput.val(button.data('value')))
  }

  $('.option-buttons .btn').on('click', function() {
    selectButton($(this));
  });

  $('.update_product_detail_variant select[class="form-control"]').on('change', function() {
    var form = $(this).closest('form');
    var data_url = $(this).attr('data-url');
    console.log(data_url)
    var hiddenInputs = form.find('input[type="hidden"]');
    var formData = form.serializeArray();
    $.each(hiddenInputsData, function(index, item) {
        formData.push(item);
    });
    console.log(formData)
    
    $.ajax({
        url: data_url,
        method: 'POST',
        data: {
            csrfmiddlewaretoken : csrfToken,
        },
        success: function(data) {
            console.log(data)
        },
        error: function(error) {
          console.log(error);
        }
    });
});







