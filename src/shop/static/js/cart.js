$(document).ready(function() {
    $('input[type="checkbox"]').click(function() {
        var cart_product_id = $(this).attr('name').split('-')[1];
        var is_checked = $(this).is(':checked');
        var update_selected_status_url = $(this).attr('data-url');
        $.ajax({
            url: update_selected_status_url,
            type: 'POST',
            data: {
                'cart_product_id': cart_product_id,
                'selected': is_checked,
                csrfmiddlewaretoken : csrfToken,
            },
            success: function(data) {
                window.location.reload();
            }
        });
    });
});

const inputNumber = document.querySelectorAll(".cart__quantity-input");
const incrementButton = document.querySelectorAll('.increment');
const decrementButton = document.querySelectorAll('.decrement');

inputNumber.forEach((number, index) => {
  if (incrementButton[index]) {
    incrementButton[index].addEventListener('click', function() {
      number.value = parseInt(number.value) + 1;
      number.dispatchEvent(new Event('change'));
    });
  }

  if (decrementButton[index]) {
    decrementButton[index].addEventListener('click', function() {
      if (number.value > 0) {
        number.value = parseInt(number.value) - 1;
        number.dispatchEvent(new Event('change'));
      }
    });
  }
});

$(document).ready(function() {
    $('.update_cart_product_quantity input[type="number"]').on('change', function() {
      var form = $(this).closest('form');
      var update_selected_status_url = $(this).attr('data-url');
      console.log(update_selected_status_url)
      $.ajax({
        url: update_selected_status_url,
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

