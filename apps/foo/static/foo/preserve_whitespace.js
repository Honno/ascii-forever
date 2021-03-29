var form = document.querySelector("form.preserve-whitespace");
var textarea = form.querySelector("textarea");

form.addEventListener("submit", function(event) {
    event.preventDefault();
    textarea.value = "." + textarea.value;
    form.submit();
});
