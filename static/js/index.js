SCROLL_RATE = 10;
KRAMER_RATE = 5000;
scrollModifier = 1;

kramers = [];

function autoBounce() {
    // change direction if we hit an edge
    if (document.body.scrollLeft == 0 ||
        document.body.scrollLeft + document.body.clientWidth == document.body.scrollWidth) {
        scrollModifier = -scrollModifier;
    }

    window.scrollBy(scrollModifier, 0);
    delay = setTimeout(autoBounce, SCROLL_RATE);
}

function getKramers() {
    $.ajax({
        url: "_getKramers",
        type: "POST",
        data: kramers
    })
    .done(res => {
        // If arrays are equal, don't update images
        if (res.kramers.join(',') == kramers.join(',')) {
            return;
        }

        kramers = res.kramers;
        // Update images
        console.log("updating! " + kramers);
    });

    delay = setTimeout(getKramers, KRAMER_RATE);
};



window.addEventListener('load', function() {
    autoBounce();
    getKramers();
});