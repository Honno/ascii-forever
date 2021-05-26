/* autosize hack */

var comment_form = document.querySelector("form.post-comment");
var comment_text = comment_form.querySelector("textarea[name='text']");
var comment_text_outer = comment_text.parentElement;

autosize(comment_text);

comment_text_outer.addEventListener("click", (e) => {
    comment_text.focus();
});

comment_text.addEventListener("focus", (e) => {
    comment_text_outer.classList.add("-focus");
});

comment_text.addEventListener("blur", (e) => {
    comment_text_outer.classList.remove("-focus");
});

/* edit feature */

var action_wrappers = document.querySelectorAll(".actions-wrapper");

action_wrappers.forEach((wrapper) => {
    let pk = parseInt(wrapper.dataset.pk);

    let actions = wrapper.querySelector(".actions");

    let edit_btn = actions.querySelector(".edit");
    if (edit_btn != null) {
        let comment_text = wrapper.querySelector(".text");

        let edit_form = wrapper.querySelector("form.edit-comment");

        let edit_text = edit_form.querySelector("textarea[name='text']");
        let edit_text_outer = edit_text.parentElement;

        let edit_text_errors = edit_form.querySelector(".text-errors");
        let edit_text_errors_ul = edit_text_errors.querySelector("ul");

        let edit_general_errors = edit_form.querySelector(".non-field-errors");
        let edit_general_errors_ul = edit_general_errors.querySelector("ul");

        autosize(edit_text);

        edit_text_outer.addEventListener("click", (e) => {
            edit_text.focus();
        });

        edit_text.addEventListener("focus", (e) => {
            edit_text_outer.classList.add("-focus");
        });

        edit_text.addEventListener("blur", (e) => {
            edit_text_outer.classList.remove("-focus");
        });

        edit_btn.addEventListener("click", (e) => {
            comment_text.classList.add("-hide");
            actions.classList.add("-hide");
            edit_form.classList.remove("-hide");
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
                        edit_text_errors.classList.add("-hide");
                        edit_text_errors_ul.innerHTML = "";
                        edit_general_errors.classList.add("-hide");
                        edit_general_errors_ul.innerHTML = "";

                        if (data.valid == true) {
                            comment_text.innerHTML = data.markup;

                            edit_form.classList.add("-hide");
                            comment_text.classList.remove("-hide");
                            actions.classList.remove("-hide");
                        } else {
                            if (data.text != undefined) {
                                data.text.forEach((error) => {
                                    let li = document.createElement("li");
                                    let li_text = document.createTextNode(error);
                                    li.appendChild(li_text);
                                    edit_text_errors_ul.appendChild(li);
                                });
                                edit_text_errors.classList.remove("-hide");
                            }

                            if (data.__all__ != undefined) {
                                data.__all__.forEach((error) => {
                                    let li = document.createElement("li");
                                    let li_text = document.createTextNode(error);
                                    li.appendChild(li_text);
                                    edit_general_errors_ul.appendChild(li);
                                });
                                edit_general_errors.classList.remove("-hide");
                            }
                        }
                    });
                })
                .catch((error) => {
                    console.error(error);
                });
        });

        let cancel_btn = edit_form.querySelector(".cancel");
        cancel_btn.addEventListener("click", (e) => {
            edit_form.classList.add("-hide");
            comment_text.classList.remove("-hide");
            actions.classList.remove("-hide");
        });
    }
});
