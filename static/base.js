document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("searchToggle").addEventListener("click", function () {
        const container = document.getElementById("search-container");
        container.style.display = container.style.display === "block" ? "none" : "block";
    });

    document.getElementById("search-form").addEventListener("submit", function (){
        
    })
    // Optional: Hide search bar if clicked outside
    document.addEventListener("click", function (event) {
        const toggle = document.getElementById("searchToggle");
        const container = document.getElementById("search-container");
        if (!container.contains(event.target) && !toggle.contains(event.target)) {
        container.style.display = "none";
        }
    });
});

function search_form(){
    search_term = document.getElementById("search-box").value;
    window.location.href = '/search_' + search_term;
}
