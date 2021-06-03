var comments = document.querySelectorAll(".comment");

comments.forEach((comment) => {
    let pk = parseInt(comment.dataset.pk);

    let text = comment.querySelector(".text");
    let actions = comment.querySelector(".actions");

    let edit_btn = actions.querySelector(".edit");
    if (edit_btn != null) {
        let edit_form = comment.querySelector("form.edit-comment");

        let edit_text = edit_form.querySelector("textarea[name='text']");
        let edit_text_outer = edit_text.parentElement;

        let edit_text_errors = edit_form.querySelector(".text-errors");
        let edit_text_errors_ul = edit_text_errors.querySelector("ul");

        let edit_general_errors = edit_form.querySelector(".non-field-errors");
        let edit_general_errors_ul = edit_general_errors.querySelector("ul");

        edit_btn.addEventListener("click", (e) => {
            text.classList.add("hide");
            actions.classList.add("hide");
            edit_form.classList.remove("hide");
        });

        edit_form.addEventListener("submit", (e) => {
            fetch("/edit_comment", {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Accept": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": Cookies.get("csrftoken"),
                },
                body: JSON.stringify({
                    "pk": pk,
                    "text": edit_text.value,
                }),
            })
                .then((response) => {
                    response.json().then((data) => {
                        edit_text_errors.classList.add("hide");
                        edit_text_errors_ul.innerHTML = "";
                        edit_general_errors.classList.add("hide");
                        edit_general_errors_ul.innerHTML = "";

                        if (data.valid == true) {
                            text.innerHTML = data.markup;

                            edit_form.classList.add("hide");
                            text.classList.remove("hide");
                            actions.classList.remove("hide");
                        } else {
                            if (data.text != undefined) {
                                data.text.forEach((error) => {
                                    let li = document.createElement("li");
                                    let li_text = document.createTextNode(error);
                                    li.appendChild(li_text);
                                    edit_text_errors_ul.appendChild(li);
                                });
                                edit_text_errors.classList.remove("hide");
                            }

                            if (data.__all__ != undefined) {
                                data.__all__.forEach((error) => {
                                    let li = document.createElement("li");
                                    let li_text = document.createTextNode(error);
                                    li.appendChild(li_text);
                                    edit_general_errors_ul.appendChild(li);
                                });
                                edit_general_errors.classList.remove("hide");
                            }
                        }
                    });
                })
                .catch((error) => {
                    console.error(error);
                });
        });

        let cancel_edit_btn = edit_form.querySelector(".cancel");
        cancel_edit_btn.addEventListener("click", (e) => {
            edit_form.classList.add("hide");
            text.classList.remove("hide");
            actions.classList.remove("hide");
        });
    }

    let delete_btn = actions.querySelector(".delete");
    if (delete_btn != null) {
        let delete_form = comment.querySelector("form.delete-comment");

        delete_btn.addEventListener("click", (e) => {
            text.classList.add("hide");
            actions.classList.add("hide");
            delete_form.classList.remove("hide");
        });

        delete_form.addEventListener("submit", (e) => {
            fetch("/delete_comment", {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Accept": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": Cookies.get("csrftoken"),
                },
                body: JSON.stringify({
                    "pk": pk,
                }),
            })
                .then((response) => {
                    response.json().then((data) => {
                        if (data.success == true) {
                            comment.classList.add("hide");
                        }
                    });
                })
                .catch((error) => {
                    console.error(error);
                });
        });

        let cancel_delete_btn = delete_form.querySelector(".cancel");
        cancel_delete_btn.addEventListener("click", (e) => {
            delete_form.classList.add("hide");
            text.classList.remove("hide");
            actions.classList.remove("hide");
        });
    }
});
