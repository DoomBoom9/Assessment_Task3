function toggle_cart_options(productId) {
    var cart_options = document.getElementById("cart_options");
    var product_quantity = document.getElementById("cart_product_quantity");
    if (cart_options.hidden == true) {
        cart_options.hidden = false;
        product_quantity.value = 1;
    }
    if (product_quantity.value <= 0) {
        cart_options.hidden = true;
        product_quantity.value = 0;  
    }
    //window.location.href = '/add_to_cart/' + productId + '_' + product_quantity.value;
}

function increase_product_quantity(productId) {
    var product_quantity = document.getElementById("cart_product_quantity");
    if (product_quantity.value <= 0) {
        toggle_cart_options(productId);
        return;
    }
    product_quantity.value = parseInt(product_quantity.value) + 1;
  //window.location.href = '/add_to_cart/' + productId + '_' + product_quantity.value;
}

function decrease_product_quantity(productId) {
    var product_quantity = document.getElementById("cart_product_quantity");
    product_quantity.value = parseInt(product_quantity.value) - 1;
    if (product_quantity.value <= 0) {
        toggle_cart_options(productId);
        return;
    }
  //window.location.href = '/add_to_cart/' + productId + '_' + product_quantity.value;
}



document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("add_to_cart").addEventListener("click", function(){
        var product_id = document.getElementById('product_id').value;
        toggle_cart_options(product_id);
    });
    document.getElementById("plus_button").addEventListener("click", function(){
        var product_id = document.getElementById('product_id').value;
        increase_product_quantity(product_id);
    });
    document.getElementById("minus_button").addEventListener("click", function(){
        var product_id = document.getElementById('product_id').value; 
        decrease_product_quantity(product_id);
    });
    document.getElementById("cart_product_quantity").addEventListener("change", function(){
        var product_id = document.getElementById('product_id').value;
        toggle_cart_options(product_id);
    });
    document.getElementById('confirm_cart').addEventListener("click", function(){
        var product_id = document.getElementById('product_id').value;
        var product_quantity = document.getElementById("cart_product_quantity");
        window.location.href = '/add_to_cart/' + product_id + '_' + product_quantity.value;
    });
});