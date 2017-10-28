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

function updateKramers() {
    kramerSpan = document.getElementById('kramers');

    // Remove all old kramers
    while (kramerSpan.hasChildNodes()) {
        kramerSpan.removeChild(kramerSpan.lastChild);
    }

    // Add all new kramers
    kramers.forEach(kramer => {
        var img = document.createElement("img");
        img.setAttribute('src', kramer);
        kramerSpan.appendChild(img);
    });
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
        updateKramers();
        // Update images
        console.log("updating! " + kramers);
    });

    delay = setTimeout(getKramers, KRAMER_RATE);
};



window.addEventListener('load', function() {
    autoBounce();
    getKramers();
});