var af_form = document.querySelector("form.preserve-whitespace");

/* js status */

var af_checkbox = af_form.querySelector("input[name='js_enabled']");
af_checkbox.value = "True";

/* whitespace preservation */

var af_textarea = af_form.querySelector("textarea[name='text']");

// if a server-side error occurs, the page is POST'd to
// browsers may carry over the dot that was prepended previously
// so we remove any such dot
// note that this may remove a legitimate dot ¯\_(ツ)_/¯
if (af_textarea.value.length > 0) {
    if (af_textarea.value[0] == ".") {
        af_textarea.value = af_textarea.value.substring(1);
    }
}

af_form.addEventListener("submit", (event) => {
    event.preventDefault();
    af_textarea.value = "." + af_textarea.value;
    af_form.submit();
});

/* thumbnail af_preview */

var af_preview = document.querySelector("pre.thumb-preview");

var x_offset_input = af_form.querySelector("input[name='thumb_x_offset']");
var x_offset_input_inc = af_form.querySelector("#x-offset-inc");
var x_offset_input_dec = af_form.querySelector("#x-offset-dec");

var y_offset_input = af_form.querySelector("input[name='thumb_y_offset']");
var y_offset_input_inc = af_form.querySelector("#y-offset-inc");
var y_offset_input_dec = af_form.querySelector("#y-offset-dec");

var af_text = af_textarea.value;

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
    let lines = af_text.split(/\r?\n/);
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
        } else {
            thumb += " ".repeat(80);
        }
        thumb += "\n";
    }

    af_preview.innerHTML = thumb;
}

render_thumb();

af_textarea.addEventListener("input", (e) => {
    af_text = e.target.value;
    render_thumb();
});

x_offset_input.addEventListener("input", (e) => {
    let n = parse_int(e.target.value);
    if (n != null) {
        x_offset = parseInt(e.target.value);
        render_thumb();
    }
});

x_offset_input_inc.addEventListener("click", (event) => {
    let cur_n = parse_int(x_offset_input.value);
    if (cur_n != null) {
        let n = cur_n + 1;
        x_offset_input.value = n;
        x_offset = n;
        render_thumb();
    }
});

x_offset_input_dec.addEventListener("click", (event) => {
    let cur_n = parse_int(x_offset_input.value);
    if (cur_n != null) {
        let n = cur_n - 1;
        x_offset_input.value = n;
        x_offset = n;
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

y_offset_input_inc.addEventListener("click", (event) => {
    let cur_n = parse_int(y_offset_input.value);
    if (cur_n != null) {
        let n = cur_n + 1;
        y_offset_input.value = n;
        y_offset = n;
        render_thumb();
    }
});

y_offset_input_dec.addEventListener("click", (event) => {
    let cur_n = parse_int(y_offset_input.value);
    if (cur_n != null) {
        let n = cur_n - 1;
        y_offset_input.value = n;
        y_offset = n;
        render_thumb();
    }
});

/* autosize */

var af_description = af_form.querySelector("textarea[name='description']");
var af_description_outer = af_description.parentElement;

autosize(af_description);

af_description.addEventListener("focus", (event) => {
    af_description_outer.classList.add("-focus");
});

af_description.addEventListener("blur", (event) => {
    af_description_outer.classList.remove("-focus");
});
