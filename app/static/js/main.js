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

    // Initialize AOS if available
    if (typeof AOS !== "undefined") {
        AOS.init({
            duration: 800,
            once: true
        });
    }

    // 🔥 Permanent Dark Mode Fix
    const savedTheme = localStorage.getItem("darkMode");

    if (savedTheme === null) {
        // Default to LIGHT mode if nothing saved
        document.body.classList.remove("dark-mode");
        localStorage.setItem("darkMode", "false");
    } 
    else if (savedTheme === "true") {
        document.body.classList.add("dark-mode");
    } 
    else {
        document.body.classList.remove("dark-mode");
    }
});


/* -----------------------------
   Toggle Dark Mode
----------------------------- */
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");

    const isDark = document.body.classList.contains("dark-mode");
    localStorage.setItem("darkMode", isDark);
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
