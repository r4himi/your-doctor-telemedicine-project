function toggleMenu() {
    const nav = document.getElementById("navMenu");
    if (nav) {
        nav.classList.toggle("active");
    } else {
        console.error("navMenu not found");
    }
}

const langBtn = document.getElementById('langBtn');
const container = document.querySelector('.language-container');

langBtn.addEventListener('click', () => {
    langBtn.style.display = container.style.display == 'flex'?'none' : 'flex';
});

document.addEventListener("DOMContentLoaded", function() {
    const dropdown = document.querySelector(".dropdown");
    const toggle = document.querySelector(".dropdown-toggle");

    toggle.addEventListener("click", function(e) {
        if (window.innerWidth <= 768) {
            e.preventDefault();
            dropdown.classList.toggle("active");
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {

    const searchInput = document.getElementById("searchInput");
    const specialitySelect = document.getElementById("specialitySelect");
    const roleSelect = document.getElementById("roleSelect");
    const langSelect = document.getElementById("langSelect");
    const allBtn = document.getElementById("allBtn");
    const cards = document.querySelectorAll(".doctor-card");

    if (!cards.length) return;

    // Collect unique values
    const specialities = new Set();
    const roles = new Set();
    const languages = new Set();

    cards.forEach(card => {
        if (card.dataset.speciality) specialities.add(card.dataset.speciality);
        if (card.dataset.role) roles.add(card.dataset.role);
        if (card.dataset.language) languages.add(card.dataset.language);
    });

    // Populate speciality select
    specialities.forEach(spec => {
        const option = document.createElement("option");
        option.value = spec;
        option.textContent = spec.charAt(0).toUpperCase() + spec.slice(1);
        specialitySelect.appendChild(option);
    });

    // Populate role select
    roles.forEach(role => {
        const option = document.createElement("option");
        option.value = role;
        option.textContent = role.charAt(0).toUpperCase() + role.slice(1);
        roleSelect.appendChild(option);
    });

    // ✅ Populate language select (based on your id="langSelect")
    languages.forEach(lang => {
        const option = document.createElement("option");
        option.value = lang;
        option.textContent = lang.charAt(0).toUpperCase() + lang.slice(1);
        langSelect.appendChild(option);
    });

    function filterDoctors() {
        const searchText = searchInput.value.toLowerCase().trim();
        const selectedSpec = specialitySelect.value.toLowerCase();
        const selectedRole = roleSelect.value.toLowerCase();
        const selectedLang = langSelect.value.toLowerCase();

        cards.forEach(card => {

            const name = card.dataset.name.toLowerCase();
            const speciality = card.dataset.speciality.toLowerCase();
            const role = card.dataset.role.toLowerCase();
            const language = card.dataset.language.toLowerCase();

            const matchesSearch =
                !searchText ||
                name.includes(searchText) ||
                speciality.includes(searchText);

            const matchesSpec =
                !selectedSpec || speciality === selectedSpec;

            const matchesRole =
                !selectedRole || role === selectedRole;

            const matchesLang =
                !selectedLang || language.includes(selectedLang);

            card.style.display =
                (matchesSearch && matchesSpec && matchesRole && matchesLang)
                ? ""
                : "none";
        });
    }

    // Event listeners
    searchInput.addEventListener("input", filterDoctors);
    specialitySelect.addEventListener("change", filterDoctors);
    roleSelect.addEventListener("change", filterDoctors);
    langSelect.addEventListener("change", filterDoctors);

    allBtn.addEventListener("click", () => {
        searchInput.value = "";
        specialitySelect.value = "";
        roleSelect.value = "";
        langSelect.value = "";
        cards.forEach(card => card.style.display = "");
    });

});




