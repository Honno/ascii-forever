var follow_button = document.querySelector("#follow-button-{{ username }}");

follow_button.addEventListener("click", (event) => {
    var follow_user = follow_button.className == "follow-button follow";

    fetch("{% url 'core:follow_user' username %}", {
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
                    follow_button.className = "follow-button unfollow";
                    follow_button.innerHTML = "Unfollow";
                } else {
                    follow_button.className = "follow-button follow";
                    follow_button.innerHTML = "Follow";
                }
            });
        })
        .catch((error) => {
            console.error(error);
        });
});
