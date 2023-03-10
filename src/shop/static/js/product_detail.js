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

const weightButtons = document.querySelectorAll('.weight-button');
const selectedWeightInput = document.querySelector('#selected-weight');

weightButtons.forEach(button => {
    button.addEventListener('click', (event) => {
        // Set the value of the selected weight input to the data-value of the clicked button
        selectedWeightInput.value = event.target.getAttribute('data-value');

        // Remove the "active" class from all weight buttons
        weightButtons.forEach(button => {
            button.classList.remove('active');
        });
        // Add the "active" class to the clicked button
        event.target.classList.add('active');
    });
});

$(document).ready(function() {
    $('.update_product_detail_variant select[class="form-control"]').on('change', function() {
      var form = $(this).closest('form');
      var data_url = $(this).attr('data-url');
      console.log(data_url)
      $.ajax({
        url: data_url,
        method: 'POST',
        data: form.serialize(),
        success: function(data) {
            window.location.reload();
        },
        error: function(error) {
          console.log(error);
        }
      });
    });
});
