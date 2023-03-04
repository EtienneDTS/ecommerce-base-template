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
                console.log(data);
            }
        });
    });
});

