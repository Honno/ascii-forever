var prose_inputs = document.querySelectorAll(".prose-input");

prose_inputs.forEach((div) => {
    let textarea = div.querySelector("textarea");

    autosize(textarea);

    div.addEventListener("click", (e) => {
        textarea.focus();
    });

    textarea.addEventListener("focus", (e) => {
        div.classList.add("-focus");
    });

    textarea.addEventListener("blur", (e) => {
        div.classList.remove("-focus");
    });
});
