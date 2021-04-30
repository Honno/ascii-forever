var arts = document.querySelectorAll(".art[data-nsfw='true']");

function blur_art() {
    arts.forEach((art) => {
        art.classList.add("-blur");
    });
}

function unblur_art() {
    arts.forEach((art) => {
        art.classList.remove("-blur");
    });
}

var blur_input = document.querySelector("#blur-toggle");

var init_blur_nsfw = Cookies.get("blur_nsfw");
if (init_blur_nsfw == "true" || typeof init_blur_nsfw == "undefined") {
    blur_input.checked = true;
    blur_art();
} else {
    blur_input.checked = false;
    unblur_art();
}

blur_input.addEventListener("change", (event) => {
    console.log(event);
    if (event.target.checked) {
        Cookies.set("blur_nsfw", "true",  { secure: true });
        blur_art();
    } else {
        Cookies.set("blur_nsfw", "false", { secure: true });
        unblur_art();
    }
});
