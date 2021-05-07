var like_spans = document.querySelectorAll(".like-actions");

like_spans.forEach((parent) => {
    let id = parent.dataset.id;

    let like_tally = parent.querySelector(".like-tally");
    let like_button = parent.querySelector(".like-button");

    like_button.addEventListener("click", (event) => {
        let like = like_button.dataset.like == "true";

        fetch("/art/" + id + "/like", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Accept": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": Cookies.get("csrftoken"),
            },
            body: JSON.stringify({"like": like}),
        })
            .then((response) => {
                response.json().then((data) => {
                    like_tally.innerHTML = data.like_tally;
                    if (data.art_liked) {
                        like_button.classList.remove("-like");
                        like_button.classList.add("-unlike");
                        like_button.dataset.like = "false";
                        like_button.innerHTML = "♥";
                    } else {
                        like_button.classList.remove("-unlike");
                        like_button.classList.add("-like");
                        like_button.dataset.like = "true";
                        like_button.innerHTML = "♡";
                    }
                });
            })
            .catch((error) => {
                console.error(error);
            });
    });
});
