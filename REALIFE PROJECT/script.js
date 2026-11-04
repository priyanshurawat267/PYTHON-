/* ================= THREE DOT MENU ================= */
const menuBtn = document.getElementById("menuBtn");
const moreMenu = document.getElementById("moreMenu");

menuBtn.addEventListener("click", () => {

    moreMenu.classList.toggle("show");
});

/* ================= SEARCH ================= */
const searchBtn = document.getElementById("searchBtn");
const searchBox = document.getElementById("searchBox");

searchBtn.addEventListener("click", () => {

    searchBox.classList.toggle("show");
});

/* ================= DARK / LIGHT ================= */
const themeBtn = document.getElementById("themeBtn");
const menuTheme = document.getElementById("menuTheme");


function setTheme() {

    document.body.classList.toggle("dark");

    const dark = document.body.classList.contains("dark");

    if (dark) {

        themeBtn.textContent = "☀️";
        menuTheme.textContent = "☀️ Light Mode";

        localStorage.setItem("theme", "dark");

    } else {

        themeBtn.textContent = "🌙";
        menuTheme.textContent = "🌙 Dark Mode";

        localStorage.setItem("theme", "light");
    }
}


themeBtn.addEventListener("click", setTheme);

menuTheme.addEventListener("click", setTheme);


/* Remember theme */

if (localStorage.getItem("theme") === "dark") {

    document.body.classList.add("dark");

    themeBtn.textContent = "☀️";
    menuTheme.textContent = "☀️ Light Mode";
}

/* ================= ADVERTISEMENT ================= */
/* Show ad after 3 seconds */

loadAdvertisement();
/* Close ad */

closeAd.addEventListener("click", () => {

    adOverlay.classList.remove("show");

});

/* Close when clicking outside */

adOverlay.addEventListener("click", (event) => {

    if (event.target === adOverlay) {

        adOverlay.classList.remove("show");

    }

});


/* Website open hote hi ad */

loadAdvertisement();


/* Close */

closeAd.addEventListener("click", () => {

    adOverlay.classList.remove("show");

});


/* Outside click */

adOverlay.addEventListener("click", (event) => {

    if (event.target === adOverlay) {

        adOverlay.classList.remove("show");
    }
});

/* Show ad after 3 seconds */

loadAdvertisement();

/* Close ad */

closeAd.addEventListener("click", () => {

    adOverlay.classList.remove("show");
});

/* Close when clicking outside */
adOverlay.addEventListener("click", (event) => {

    if (event.target === adOverlay) {

        adOverlay.classList.remove("show");
    }
});

/* ================= MENU OPTIONS ================= */
function openGmail() {

    window.location.href =
        "mailto:codeacademy@gmail.com";
}

function openMap() {

    window.open(
        "https://www.google.com/maps/search/?api=1&query=Code+Academy",
        "_blank"
    );
}


function openContact() {

    document.getElementById("modalTitle").textContent =
        "Contact Code Academy";

    document.getElementById("modalText").textContent =
        "Email: codeacademy@gmail.com | Phone: +91 98765 43210";

    document.getElementById("modal").classList.add("show");

}

function showNotification() {

    document.getElementById("modalTitle").textContent =
        "Notifications";

    document.getElementById("modalText").textContent =
        "🎉 New Python course is available!";

    document.getElementById("modal").classList.add("show");

}

function showSettings() {

    document.getElementById("modalTitle").textContent =
        "Settings";

    document.getElementById("modalText").textContent =
        "Theme and website preferences.";

    document.getElementById("modal").classList.add("show");

}

function showAbout() {

    document.getElementById("modalTitle").textContent =
        "About Code Academy";

    document.getElementById("modalText").textContent =
        "Code Academy is a learning platform for programming students.";

    document.getElementById("modal").classList.add("show");

}

function closeModal() {

    document.getElementById("modal").classList.remove("show");

}
