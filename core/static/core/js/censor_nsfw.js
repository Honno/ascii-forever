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

    let show = actions.querySelector(".nsfw-show");
    show.addEventListener("click", (e) => {
        actions.classList.add("hide");
        art.classList.remove("hide");
    });
});

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
        });
    })
    .catch((error) => {
        console.error(error);
    });
