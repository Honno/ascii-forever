var follow_buttons = document.querySelectorAll(".follow-button");

follow_buttons.forEach((button) => {
    let id_words = button.id.split("-");
    let username = id_words[id_words.length - 1];

    button.addEventListener("click", (event) => {
        let follow_user = button.classList.contains("follow");

        fetch("/users/" + username + "/follow", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Accept": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": Cookies.get("csrftoken"),
            },
            body: JSON.stringify({"follow_user": follow_user}),
        })
            .then((response) => {
                response.json().then((data) => {
                    if (data.user_followed) {
                        button.classList.remove("follow");
                        button.classList.add("unfollow");
                        button.innerHTML = "Unfollow";
                    } else {
                        button.classList.remove("unfollow");
                        button.classList.add("follow");
                        button.innerHTML = "Follow";
                    }
                });
            })
            .catch((error) => {
                console.error(error);
            });
    });
});
