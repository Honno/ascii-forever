var like_spans = document.querySelectorAll(".art-like");

like_spans.forEach((parent) => {
    let id_words = parent.id.split("-");
    let id = id_words[id_words.length - 1];

    let like_tally = parent.querySelector(".art-like-tally");
    let like_button = parent.querySelector(".like-art");

    like_button.addEventListener("click", (event) => {
        let like = like_button.classList.contains("like");

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
                        like_button.classList.remove("like");
                        like_button.classList.add("unlike");
                        like_button.innerHTML = "Unlike";
                    } else {
                        like_button.classList.remove("unlike");
                        like_button.classList.add("like");
                        like_button.innerHTML = "Like";
                    }
                });
            })
            .catch((error) => {
                console.error(error);
            });
    });
});
