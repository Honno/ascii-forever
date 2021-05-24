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

