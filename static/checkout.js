const same_address = document.getElementById("same-address")
const shipping_address_details = document.getElementById("shipping-address-details")

document.addEventListener("DOMContentLoaded", function() {

    document.getElementById("same-address").addEventListener("click", function(){
        if (same_address.checked) {
            shipping_address_details.hidden = true
        } else {
            shipping_address_details.hidden = false
        }
    });
}); 