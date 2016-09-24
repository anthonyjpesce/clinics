/* Copyright Anthony J. Pesce and Jon Schleuss */

document.getElementById('find_locations').onclick=function(){
    console.log('find location');
    getLocation(); // get users location

    loadClinics(); // will be moved
};

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        console.log("Geolocation is not supported by this browser.");
    }
}
function showPosition(position) {
    console.log(position.coords.latitude + "," + position.coords.longitude);
}

// get list of clinics that match
function loadClinics() {
    // hide init header and button
    $("#ini-content").fadeOut(400, function(){
        // after init content disappears
        $(".navbar").fadeIn(400);
    });

    // alter top of page for search results
    // add filter options

    // create list
    $.getJSON( "/static/js/90029-50-more-data.json", function( data ) {
        console.log(data);
    });
}

