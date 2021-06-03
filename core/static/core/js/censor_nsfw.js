var nsfw_art_thumbs = document.querySelectorAll(".art-thumb[data-nsfw='true'], .user-art-thumb[data-nsfw='true']");
var nsfw_arts = document.querySelectorAll(".art-container[data-nsfw='true']");

var nsfwables = [];
nsfwables.push.apply(nsfwables, nsfw_art_thumbs);
nsfwables.push.apply(nsfwables, nsfw_arts);

function show_all() {
    nsfwables.forEach((thumb) => {
        thumb.classList.remove("hide");

        let actions = thumb.querySelector(".nsfw-actions");
        let art = thumb.querySelector(".art");

        actions.classList.add("hide");
        art.classList.remove("hide");
    });
}

function hide_all() {
    // all expanded arts should be accessible, hence only hiding the thumbs
    nsfw_art_thumbs.forEach((thumb) => {
        thumb.classList.add("hide");
    });
}

nsfwables.forEach((thumb) => {
    let actions = thumb.querySelector(".nsfw-actions");
    let art = thumb.querySelector(".art");

    let cookie_name = "show_nsfw_" + thumb.dataset.pk;
    let cookie = Cookies.get(cookie_name);
    if (cookie == "true") {
        actions.classList.add("hide");
        art.classList.remove("hide");
    } else {
        let show = actions.querySelector(".nsfw-show");
        show.addEventListener("click", (e) => {
            actions.classList.add("hide");
            art.classList.remove("hide");

            Cookies.set(cookie_name, "true", {secure: true, expires: 1});
        });
    }
});

/* Applying user preferences */

// Try short-circuiting with cookies first

var saved_nsfw_pref = Cookies.get("nsfw_pref");

if (typeof saved_nsfw_pref == "undefined" || saved_nsfw_pref == "HA") {
    hide_all();
} else if (saved_nsfw_pref == "HA") {
    show_all();
}

// Then check with the server

fetch("/nsfw_pref", {
    method: "GET",
    credentials: "same-origin",
    headers: {
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": Cookies.get("csrftoken"),
    }
})
    .then((response) => {
        response.json().then((data) => {
            if (data.nsfw_pref == "SA") {
                show_all();
            } else if (data.nsfw_pref == "HA") {
                hide_all();
            }

            if (saved_nsfw_pref != data.nsfw_pref) {
                Cookies.set("nsfw_pref", data.nsfw_pref, { secure: true });
            }
        });
    })
    .catch((error) => {
        console.error(error);
    });
