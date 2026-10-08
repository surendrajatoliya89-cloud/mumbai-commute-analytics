/* 
 * script.js
 * Client-side interactivity and table search/filter helpers
 * College Project - B.Sc Data Science
 */

document.addEventListener("DOMContentLoaded", function () {
    console.log("Mumbai Commute Analytics UI Loaded.");

    // Table search filter for data.html
    const searchInput = document.getElementById("tableSearch");
    if (searchInput) {
        searchInput.addEventListener("keyup", function () {
            const filter = searchInput.value.toLowerCase();
            const rows = document.querySelectorAll("#commuteTable tbody tr");

            rows.forEach(function (row) {
                const text = row.textContent.toLowerCase();
                if (text.includes(filter)) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }
            });
        });
    }

    // Auto-dismiss alerts after 5 seconds if any
    const alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

