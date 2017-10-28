SCROLL_RATE = 10;
scrollModifier = 1;

function scroll() {
    if (document.body.scrollLeft == 0 ||
        document.body.scrollLeft + document.body.clientWidth == document.body.scrollWidth) {
        scrollModifier = -scrollModifier;
    }
    window.scrollBy(scrollModifier, 0);
    scrolldelay = setTimeout(scroll, SCROLL_RATE);
}

window.addEventListener('load', scroll);