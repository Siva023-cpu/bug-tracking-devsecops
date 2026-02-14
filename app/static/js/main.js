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
   Initialize AOS Animation
----------------------------- */
document.addEventListener("DOMContentLoaded", function () {
    if (typeof AOS !== "undefined") {
        AOS.init({
            duration: 800,
            once: true
        });
    }

    // Load Dark Mode Preference
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark-mode");
    }
});


/* -----------------------------
   Toggle Dark Mode
----------------------------- */
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");

    localStorage.setItem(
        "darkMode",
        document.body.classList.contains("dark-mode")
    );
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
