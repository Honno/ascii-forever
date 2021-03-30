var form = document.querySelector("form.preserve-whitespace");
var textarea = form.querySelector("textarea");

// if a server-side error occurs, the page is POST'd to
// browsers may carry over the dot that was prepended previously
// so we remove any such dot
// note that this may remove a legitimate dot ¯\_(ツ)_/¯
if (textarea.value.length > 0) {
    if (textarea.value[0] == ".") {
        textarea.value = textarea.value.substring(1);
    }
}

form.addEventListener("submit", function(event) {
    event.preventDefault();
    textarea.value = "." + textarea.value;
    form.submit();
});
