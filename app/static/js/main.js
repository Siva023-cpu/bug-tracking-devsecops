console.log("Bug Tracker Loaded");

/* -----------------------------
   Auto-hide Alerts
----------------------------- */
setTimeout(function () {
    let alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
        alert.style.display = "none";
    });
}, 4000);


/* -----------------------------
   Initialize Page
----------------------------- */
document.addEventListener("DOMContentLoaded", function () {

    // Initialize AOS safely
    if (typeof AOS !== "undefined") {
        AOS.init({
            duration: 800,
            once: true
        });
    }

    /* -----------------------------
       Load Saved Theme
    ----------------------------- */
    const savedTheme = localStorage.getItem("theme") || "light";

    // Apply saved theme
    document.documentElement.setAttribute("data-bs-theme", savedTheme);

    // Update icon on page load
    const icon = document.getElementById("themeIcon");
    if (icon) {
        if (savedTheme === "dark") {
            icon.classList.remove("fa-moon");
            icon.classList.add("fa-sun");
        } else {
            icon.classList.remove("fa-sun");
            icon.classList.add("fa-moon");
        }
    }
});


/* -----------------------------
   Toggle Dark Mode (Bootstrap 5.3)
----------------------------- */
function toggleDarkMode() {

    const html = document.documentElement;
    const icon = document.getElementById("themeIcon");

    const currentTheme = html.getAttribute("data-bs-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";

    // Set new theme
    html.setAttribute("data-bs-theme", newTheme);

    // Save to localStorage
    localStorage.setItem("theme", newTheme);

    // Change icon
    if (icon) {
        if (newTheme === "dark") {
            icon.classList.remove("fa-moon");
            icon.classList.add("fa-sun");
        } else {
            icon.classList.remove("fa-sun");
            icon.classList.add("fa-moon");
        }
    }
}


/* -----------------------------
   Toggle Password Visibility
----------------------------- */
function togglePassword(inputId, iconSpan) {
    const input = document.getElementById(inputId);
    const icon = iconSpan.querySelector("i");

    if (!input) return;

    if (input.type === "password") {
        input.type = "text";
        if (icon) icon.classList.replace("fa-eye", "fa-eye-slash");
    } else {
        input.type = "password";
        if (icon) icon.classList.replace("fa-eye-slash", "fa-eye");
    }
}
