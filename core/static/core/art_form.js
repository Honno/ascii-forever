var form = document.querySelector("form.preserve-whitespace");

/* JS status */

var element = form.querySelector(".no-js-warn");
element.style.display = "none";

var checkbox = form.querySelector("input[name='js_enabled']");
checkbox.value = "True";

/* Whitespace preservation */

var textarea = form.querySelector("textarea[name='text']");

// if a server-side error occurs, the page is POST'd to
// browsers may carry over the dot that was prepended previously
// so we remove any such dot
// note that this may remove a legitimate dot ¯\_(ツ)_/¯
if (textarea.value.length > 0) {
    if (textarea.value[0] == ".") {
        textarea.value = textarea.value.substring(1);
    }
}

form.addEventListener("submit", (event) => {
    event.preventDefault();
    textarea.value = "." + textarea.value;
    form.submit();
});

/* Thumbnail preview */

var preview = document.querySelector("pre.thumb-preview");

var x_offset_input = form.querySelector("input[name='thumb_x_offset']");
var y_offset_input = form.querySelector("input[name='thumb_y_offset']");

var text = textarea.value;
var x_offset = parseInt(x_offset_input.value);
var y_offset = parseInt(y_offset_input.value);

function render_thumb() {
    let lines = text.split(/\r?\n/);
    let thumb = "";

    for (let y = y_offset; y < y_offset + 19; y++) {
        let line = lines[y];
        if (typeof line !== "undefined") {
            for (let x = x_offset; x < x_offset + 80; x++) {
                let char = line[x];
                if (typeof char !== "undefined") {
                    thumb += char;
                } else {
                    thumb += " ";
                }
            }
        }
        thumb += "\n";
    }

    preview.innerHTML = thumb;
}

render_thumb();

textarea.addEventListener("input", (e) => {
    text = e.target.value;
    render_thumb();
});

x_offset_input.addEventListener("input", (e) => {
    x_offset = parseInt(e.target.value);
    render_thumb();
});

y_offset_input.addEventListener("input", (e) => {
    y_offset = parseInt(e.target.value);
    render_thumb();
});

