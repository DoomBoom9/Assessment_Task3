const checkboxes = document.querySelectorAll('.category-check');
const productItems = document.querySelectorAll('.product-item');
const resetBtn = document.getElementById('resetFilters');


function toggle_cart_options(productId) {
    var cart_options = document.getElementById("cart_options_" + productId);
    var product_quantity = document.getElementById("cart_product_quantity_" + productId);
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
    var product_quantity = document.getElementById("cart_product_quantity_" + productId);
    if (product_quantity.value <= 0) {
        toggle_cart_options(productId);
        return;
    }
    product_quantity.value = parseInt(product_quantity.value) + 1;
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

function event_listener_id() {
    var product_id = event.target.id.match(/(\d+)/)[0];
    return product_id;
}

document.addEventListener("DOMContentLoaded", function() {
    for (var i = 1; i <= document.getElementById('number_of_categories').value; i++){
        var category = document.querySelectorAll(`[data-category="${i}"]`);
        document.getElementById(`cat_${i}_text`).innerHTML = `(${category.length})`;
    }
    
    for (var i = 1; i <= document.getElementById('number_of_products').value; i++) { 
        document.getElementById("add_to_cart_" + i).addEventListener("click", function(){
            var product_id = event_listener_id();
            toggle_cart_options(product_id);
        });
        document.getElementById("plus_button_"+i).addEventListener("click", function(){
            var product_id = event_listener_id();
            increase_product_quantity(product_id);
        });
        document.getElementById("minus_button_"+i).addEventListener("click", function(){
            var product_id = event_listener_id();
            decrease_product_quantity(product_id);
        });
        document.getElementById("cart_product_quantity_" + i).addEventListener("change", function(){
            var product_id = event_listener_id();
            toggle_cart_options(product_id);
        });
        document.getElementById('confirm_cart_' + i).addEventListener("click", function(){
            var product_id = event_listener_id();
            var product_quantity = document.getElementById("cart_product_quantity_" + product_id);
            window.location.href = '/add_to_cart/' + product_id + '_' + product_quantity.value;
        });
    }

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const checked = Array.from(checkboxes).filter(cb => cb.checked).map(cb => cb.value);
            productItems.forEach(item => {
                const category = item.getAttribute('data-category');
                item.style.display = (checked.length === 0 || checked.includes(category)) ? 'block' : 'none';
            });
        });
    });

    resetBtn.addEventListener('click', e => {
        e.preventDefault();
        checkboxes.forEach(cb => cb.checked = false);
        productItems.forEach(item => item.style.display = 'block');
    });
        

}); 
