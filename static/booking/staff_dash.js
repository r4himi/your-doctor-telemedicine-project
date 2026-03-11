document.addEventListener("DOMContentLoaded", () => {
    const filterDate = document.getElementById("filterDate");
    const todayBtn = document.getElementById("todayBtn");
    const tomorrowBtn = document.getElementById("tomorrowBtn");
    const yesterdayBtn = document.getElementById("yesterdayBtn");
    const rows = document.querySelectorAll(".appointments-table tbody tr");

    function formatDate(date) {
        const yyyy = date.getFullYear();
        const mm = String(date.getMonth() + 1).padStart(2, "0");
        const dd = String(date.getDate()).padStart(2, "0");
        return `${yyyy}-${mm}-${dd}`;
    }

    function filterRowsByDate(selectedDate) {
        rows.forEach(row => {
            const rowDate = row.dataset.date;
            row.style.display = (rowDate === selectedDate) ? "" : "none";
        });
    }

    // Set quick buttons
    const today = new Date();
    const todayStr = formatDate(today);

    todayBtn.addEventListener("click", () => {
        filterDate.value = todayStr;
        filterRowsByDate(todayStr);
    });

    const tomorrow = new Date();
    tomorrow.setDate(today.getDate() + 1);
    const tomorrowStr = formatDate(tomorrow);
    tomorrowBtn.addEventListener("click", () => {
        filterDate.value = tomorrowStr;
        filterRowsByDate(tomorrowStr);
    });

    const yesterday = new Date();
    yesterday.setDate(today.getDate() - 1);
    const yesterdayStr = formatDate(yesterday);
    yesterdayBtn.addEventListener("click", () => {
        filterDate.value = yesterdayStr;
        filterRowsByDate(yesterdayStr);
    });

    // Date picker change
    filterDate.addEventListener("change", () => {
        filterRowsByDate(filterDate.value);
    });

    // Initially show today
    filterRowsByDate(todayStr);
});