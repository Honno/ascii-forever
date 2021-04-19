var like_tally = document.querySelector("#art-like-tally-{{ pk }}");
var like_button = document.querySelector("#like-art-{{ pk }}");

like_button.addEventListener("click", (event) => {
    let like = like_button.className == "like-art like";

    fetch("{% url 'core:like_art' pk %}", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": get_cookie("csrftoken"),
        },
        body: JSON.stringify({"like": like}),
    })
        .then((response) => {
            response.json().then((data) => {
                like_tally.innerHTML = data.like_tally;
                if (data.art_liked) {
                    like_button.className = "like-art unlike";
                    like_button.innerHTML = "Unlike";
                } else {
                    like_button.className = "like-art like";
                    like_button.innerHTML = "Like";
                }
            });
        })
        .catch((error) => {
            console.error(error);
        });
});
