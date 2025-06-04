

function increase_product_quantity(productId) {
    var product_quantity = document.getElementById("cart_product_quantity_" + productId);
    var quantity_in_cart = document.getElementById("qty_"+ productId).value; // find the qty of the product with id product_id.

    if (parseInt(product_quantity.value) <= 0) {
        toggle_cart_options(productId);
        return;
    }
    if (parseInt(product_quantity.value) > quantity_in_cart){
        product_quantity.value = quantity_in_cart;
        return;
    }

    if ((parseInt(product_quantity.value) < quantity_in_cart) && (parseInt(product_quantity.value) > 0)){
        product_quantity.value ++;
    }
    
  //window.location.href = '/add_to_cart/' + productId + '_' + product_quantity.value;
}

function decrease_product_quantity(productId) {
    var product_quantity = document.getElementById("cart_product_quantity_" + productId);
    product_quantity.value = parseInt(product_quantity.value) - 1;
    if (product_quantity.value <= 0) {
        toggle_cart_options(productId);
        return;
    }
  //window.location.href = '/add_to_cart/' + productId + '_' + product_quantity.value;
}
function toggle_cart_options(productId) {
    var cart_options = document.getElementById("cart_options_" + productId);
    var product_quantity = document.getElementById("cart_product_quantity_" + productId);
    if (cart_options.hidden == true) {
        cart_options.hidden = false;
        product_quantity.value = 1;
    }
    if (parseInt(product_quantity.value) <= 0) {
        cart_options.hidden = true;
        product_quantity.value = 0;  
    }
    //window.location.href = '/add_to_cart/' + productId + '_' + product_quantity.value;
}
function event_listener_id() {
    var product_id = event.target.id.match(/(\d+)/)[0];
    return product_id;
}

//number of products will have to change.
// can be dervied from the product id getting process?
// 
document.addEventListener("DOMContentLoaded", function() {
    const slides = document.getElementsByClassName("product_ids");
    for (let i = 0; i < slides.length; i++) {
        var product_id = slides.item(i).value
        document.getElementById('remove_'+ product_id).addEventListener("click", function(){
            var product_id = event_listener_id();
            toggle_cart_options(product_id);
        })
    
        document.getElementById("plus_button_" + product_id).addEventListener("click", function(){
            var product_id = event_listener_id();
            increase_product_quantity(product_id);
        });
        document.getElementById("minus_button_"+ product_id).addEventListener("click", function(){
            var product_id = event_listener_id();
            decrease_product_quantity(product_id);
        });
        document.getElementById("cart_product_quantity_" + product_id).addEventListener("change", function(){
            var product_id = event_listener_id();
            var product_quantity = document.getElementById("cart_product_quantity_" + product_id);
            var quantity_in_cart = document.getElementById("qty_"+ product_id).value;
            
            if (parseInt(product_quantity.value) > quantity_in_cart){
                
                product_quantity.value = quantity_in_cart;
            }
            toggle_cart_options(product_id);
        });

        document.getElementById('confirm_' + product_id).addEventListener("click", function(){
            var product_id = event_listener_id();
            var product_quantity = document.getElementById("cart_product_quantity_" + product_id);
            window.location.href = '/remove_from_cart/' + product_id + '_' + product_quantity.value;
        });
    
    }
    
    
    
});