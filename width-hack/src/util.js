export function addNewChild(element, tag, styles, text) {
    let elm = makeElement(tag, styles, text);
    element.appendChild(elm);
    return elm;
}

export function makeElement(tag, styles, text) {
    let elm = document.createElement(tag);
    style(elm, styles);
    if (text) {
        elm.innerHTML = text;
    }
    return elm;
}

export function style(element, styles) {
    if (!styles) {
        return
    }
    for (const [key, value] of Object.entries(styles)) {
        element.style[key] = value;
    }
    return element;
}

export function makeFunctionalDemo(html, centerContainer) {
    let container = makeElement("div", {"text-indent": "0"});
    if (centerContainer) {
        container.style["align-self"] = "center";
    }
    container.innerHTML = html;
    return container;
}

export function makeHtmlDemo(html, centerContainer) {
    let fonts = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'liberation mono', 'courier new', monospace";
    let container = makeElement("span", {"padding": "8px", "padding-bottom": "-1rem", "width": "100%", "overflow": "auto", "background": "rgb(31, 41, 55)", "color": "rgb(299, 231, 235)", "border-radius": "8px", "font-size": "13px", "font-family": fonts, "white-space": "pre", "text-indent": "0", "line-height": "1.2"});
    if (centerContainer) {
        container.style["align-self"] = "center";
    }
    
    let parsedHtml = html.replaceAll("<", "&lt;");
    parsedHtml = parsedHtml.replaceAll(">", "&gt;");
    
    while (parsedHtml.includes("[")) {
        let start = parsedHtml.indexOf("[");
        let end = parsedHtml.indexOf("]");
        let excise = parsedHtml.substring(start, end);
        let color = excise.split(" ")[0];
        excise = excise.replace(color + " ", "");
        color = color.substring(1);
        parsedHtml = replaceFromIndicesWith(parsedHtml, start, end, "<span style='color:" + color + "'>" + excise + "</span>");
    }
    container.innerHTML = parsedHtml;
    return container;
}

export function replaceFromIndicesWith(string, start, end, newString) {
    return string.substring(0, start) + newString + string.substring(end + 1);
}

export function formatText(text) {
    let replacements = {"!hero": "<span style='text-decoration: underline solid #83254f; text-decoration-thickness: 2px '>hero</span>",
                        "!memory": "<span style='text-decoration: underline solid turquoise; text-decoration-thickness: 2px '>memory</span>",
                        "!button": "<span style='text-decoration: underline solid plum; text-decoration-thickness: 2px '>button</span>"};
    let out = text;
    for (const term in replacements) {
        while (out.includes(term)) {
            let start = out.indexOf(term);
            let end = start + term.length - 1;
            out = replaceFromIndicesWith(out, start, end, replacements[term]);
        }
    }
    return out;
}