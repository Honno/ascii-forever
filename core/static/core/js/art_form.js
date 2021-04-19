var form = document.querySelector("form.preserve-whitespace");

/* js status */

var element = form.querySelector(".no-js-warn");
element.style.display = "none";

var checkbox = form.querySelector("input[name='js_enabled']");
checkbox.value = "True";

/* whitespace preservation */

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

/* thumbnail preview */

var preview = document.querySelector("pre.thumb-preview");

var x_offset_input = form.querySelector("input[name='thumb_x_offset']");
var y_offset_input = form.querySelector("input[name='thumb_y_offset']");

var text = textarea.value;

function parse_int(value) {
    if (isNaN(value))
        return null;

    if (value == "")
        return null;

    let n = parseInt(value);

    if (!isFinite(n))
        return null;

    return n;
}

var x_offset = parse_int(x_offset_input.value);
var y_offset = parse_int(y_offset_input.value);

// on page reloads these values could be non-integers
if (x_offset == null)
    x_offset = 0;
if (y_offset == null)
    y_offset = 0;

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
    let n = parse_int(e.target.value);
    if (n != null) {
        x_offset = parseInt(e.target.value);
        render_thumb();
    }
});

y_offset_input.addEventListener("input", (e) => {
    let n = parse_int(e.target.value);
    if (n != null) {
        y_offset = parseInt(e.target.value);
        render_thumb();
    }
});

