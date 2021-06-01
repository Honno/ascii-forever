var preserve_whitespace_forms = document.querySelectorAll("form.preserve-whitespace");

preserve_whitespace_forms.forEach((form) => {
    let textarea = form.querySelector("textarea.dot-prepend");

    // if a server-side error occurs, the page is POST'd to
    // browsers may carry over the dot that was prepended previously
    // so we remove any such dot
    // note that this may remove a legitimate dot ¯\_(ツ)_/¯
    if (textarea.value.length > 0) {
        if (textarea.value[0] == ".") {
            textarea.value = textarea.value.substring(1);
        }
    }

    let checkbox = form.querySelector("input[name='js_enabled']");
    checkbox.value = "True";

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        textarea.value = "." + textarea.value;
        form.submit();
    });
});
