SCROLL_RATE = 50;
KRAMER_RATE = 1000;
scrollModifier = 1;
kramers = [];

// Ping pong scroll the family portrait
function autoBounce() {
    // change direction if we hit an edge
    if (document.body.scrollLeft == 0 ||
        document.body.scrollLeft + document.body.clientWidth == document.body.scrollWidth) {
        scrollModifier = -scrollModifier;
    }

    window.scrollBy(scrollModifier, 0);
    delay = setTimeout(autoBounce, SCROLL_RATE);
}

// Update kramer images
function updateKramers() {
    kramerSpan = document.getElementById('kramers');
    // Remove all old kramers
    while (kramerSpan.hasChildNodes()) {
        kramerSpan.removeChild(kramerSpan.lastChild);
    }

    // Add all new kramers
    kramers.forEach((kramer, i) => {
        var img = document.createElement("img");
        img.setAttribute('src', kramer);

        if (i == 0) {
            console.log('hey');
            var a = document.createElement("a");
            a.setAttribute('href', '_stream');
            a.appendChild(img);
            kramerSpan.appendChild(a);
        } else {
            kramerSpan.appendChild(img);
        }
    });
}

// Get kramer list
function getKramers() {
    // Send AJAX query
    $.ajax({ url: "_getKramers", type: "POST" }).done(res => {
        // If arrays are equal, don't update images
        if (res.kramers.join(',') == kramers.join(',')) {
            return;
        }

        // Update kramers
        kramers = res.kramers;
        updateKramers();
    });

    delay = setTimeout(getKramers, KRAMER_RATE);
};

// Set up
window.addEventListener('load', function() {
    autoBounce();
    getKramers();
});