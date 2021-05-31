var follow_buttons = document.querySelectorAll(".follow-button");

follow_buttons.forEach((button) => {
    let username = button.dataset.username;

    button.addEventListener("click", (event) => {
        let follow_user = button.dataset.follow == "true";

        fetch("/user/" + username + "/follow", {
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
                        button.classList.add("-negative");
                        button.dataset.follow = "false";
                        button.innerHTML = "Unfollow";
                    } else {
                        button.classList.remove("-negative");
                        button.dataset.follow = "true";
                        button.innerHTML = "Follow";
                    }
                });
            })
            .catch((error) => {
                console.error(error);
            });
    });
});
