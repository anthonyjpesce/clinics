/* Copyright Anthony J. Pesce and Jon Schleuss */

document.getElementById('find-locations').onclick=function(){
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

function showList() {
    // create list
    $.getJSON( "/static/js/90029-50-more-data.json", function( data ) {
        console.log(data);

        // CHECK IF ANY ARE OPEN TODAY AND NOW
        $("#results-list").append("<p>These clinics are open now:</p>");
        // $("#results-list").append("<p>No nearby clinics are open now. These will be open tomorrow:</p>");
        // $("#results-list").append("<p>No nearby clinics are open now. These will be open on TK:</p>");

        // populate list
        var items = [];
        $.each( data, function( key, val ) {
            var milesText = (key === 0) ? " miles" : ""; // show miles on first
            items.push( "<li id='" + key + "'><span class='clinic-name'>" + val.name + "</span><span class='clinic-distance'>" + key + ".2" + milesText + "</span></li>" );
        });

        $( "<ol/>", {
            "class": "my-new-list",
            html: items.join( "" )
        }).appendTo( "#results-list" );

        // add map
        $("#results-list").append("<div id='map'></div>");

        $("#results-list").fadeIn(400);

    });
}

// get list of clinics that match
function loadClinics() {
    // hide init header and button
    $("#ini-content").fadeOut(400, function(){
        // after init content disappears
        $(".navbar").fadeIn(400);
        showList();
    });

    // alter top of page for search results
    // add filter options


}

