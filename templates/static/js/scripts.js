/* By Anthony J. Pesce and Jon Schleuss */

var windowWidth = document.documentElement.clientWidth;


// listen for user to try find location
$('#find-location').on('click touchstart',function(){
    alert("finding location");
    console.log('finding location');
    getLocation(); // get users location
});
// document.getElementById('find-location').onclick=function(){

// };


// gets user's location
function getLocation() {
    if (navigator.geolocation) {
        // console.log(navigator.geolocation.getCurrentPosition());
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        console.log("Geolocation is not supported by this browser.");
    }
}


function showPosition(position) {
    console.log(position.coords.latitude + "," + position.coords.longitude);

    var coords = [position.coords.latitude,position.coords.longitude];
    loadClinics(coords);
}

function loadClinics(coords) {
    // hide init header and button
    $(".init-content").fadeOut(400, function(){
        // after init content disappears
        $(".navbar-default").css({
           'border' : '1px solid #e7e7e7',
           'background-color' : '#f8f8f8',
           'margin' : '0 0 20px'
        });
    });

    // alter top of page for search results
    // add filter options

    // create list
    $.getJSON( "/api/clinics/?format=json&lat="+coords[0]+"&lon="+coords[1], function( data ) {
    // $.getJSON( "/static/js/90029-50-more-data.json", function( data ) {
        console.log(data);

        data = data['results']

        console.log('adding filters');
        // // add filter options list
        var filters = [];
        $.each( data, function( key, val ) {
            for (var j = 0; j < val.categories.length; j++) {
                var filterItem = "<li class='filter-option'>" + val.categories[j] + "</li>";

                // check that it's not already in the list
                if (filters.indexOf(filterItem) == -1) {
                    filters.push(filterItem);
                }
            }
        });

        $("#results-list").append("<p>Filter:</p>");

        $( "<ul/>", {
            "id": "filter-list",
            html: filters.join( "" )
        }).appendTo( "#results-list" );

        filterListener(coords);

        // CHECK IF ANY ARE OPEN TODAY AND NOW
        $("#results-list").append("<p class='open-close-note'><span class='clinic-status-icon clinic-open'></span>These clinics are open now<br><span class='clinic-status-icon clinic-closed'></span>These are currently closed</p>");
        // $("#results-list").append("<p>No nearby clinics are open now. These will be open tomorrow:</p>");
        // $("#results-list").append("<p>No nearby clinics are open now. These will be open on TK:</p>");

        // populate list
        var items = [];
        $.each( data, function( key, val ) {
            // figure out if clinic is open for user's time
            // if open today
            if (val.hours[userDay.toLowerCase()] != false) {
                var openTime = +(val.hours[userDay.toLowerCase()].open.substring(0,2)+val.hours[userDay.toLowerCase()].open.substring(3,5));
                var closeTime = +(val.hours[userDay.toLowerCase()].close.substring(0,2)+val.hours[userDay.toLowerCase()].close.substring(3,5));
                var userTime = +(d.getHours().toString()+d.getMinutes().toString());

                console.log(val.hours[userDay.toLowerCase()]);
            }

            var clinicStatus = (val.hours[userDay.toLowerCase()] === false) ? "clinic-closed" :
                               (openTime < userTime && userTime < closeTime) ? "clinic-open" : "clinic-closed";


            var milesText = (windowWidth > 768) ? " miles" :
                            (key === 0) ? " miles" : ""; // show miles on first
            items.push( "<li id='" + key + "' class='" + clinicStatus + "'><span class='clinic-name'><a href='"+val.href+"'>" + val.name + "</a></span><span class='clinic-distance'>" + val.distance.toFixed(1) + milesText + "</span></li>" );
        });

        $( "<ol/>", {
            "class": "my-new-list",
            html: items.join( "" )
        }).appendTo( "#results-list" );

        // add map
        $("#results-list").append("<div id='map'></div>");

        $("#results-list").fadeIn(400, function() {

            mapboxgl.accessToken = 'pk.eyJ1Ijoic2NobGV1c3MiLCJhIjoicEtaaE54cyJ9.PWSVNlOtpDp0x1phUruQ9g';
            var map = new mapboxgl.Map({
                container: 'map', // container id
                style: 'mapbox://styles/mapbox/light-v9', //stylesheet location
                center: [coords[1], coords[0]], // starting position
                zoom: 10 // starting zoom
            });

            // add markers of points
            for (var i = 0; i < data.length; i++) {

                var val = data[i];

                if (val.hours[userDay.toLowerCase()] != false) {
                    var openTime = +(val.hours[userDay.toLowerCase()].open.substring(0,2)+val.hours[userDay.toLowerCase()].open.substring(3,5));
                    var closeTime = +(val.hours[userDay.toLowerCase()].close.substring(0,2)+val.hours[userDay.toLowerCase()].close.substring(3,5));
                    var userTime = +(d.getHours().toString()+d.getMinutes().toString());
                }

                var markerStatus = (val.hours[userDay.toLowerCase()] === false) ? "marker-closed" :
                               (openTime < userTime && userTime < closeTime) ? "marker-open" : "marker-closed";

                var el = document.createElement('a');
                el.className = 'marker ' + markerStatus;
                el.href = val.href;
                new mapboxgl.Marker(el)
                .setLngLat([data[i].location[1],data[i].location[0]])
                .addTo(map);

            }


            // markers.push(marker);

            // disable map zoom when using scroll
            map.scrollZoom.disable();

        });

    });
}

$("#geocodify-basic-box").geocodify({
    onSelect: function (result) { 
        var coords = [result.geometry.location.lat(),
                result.geometry.location.lng()];

        // get clinics
        loadClinics(coords);
    }
});

function filterListener(coords) {
    $('.filter-option').on('click touchstart',function(){
        var filterSel = this.innerHTML;

        // update class
        $('.filter-option').removeClass('filter-selected');
        $(this).addClass('filter-selected');

        // console.log("/api/clinics/?format=json&lat="+coords[0]+"&lon="+coords[1]+"&categories="+filterSel);

        // get new data
        $.getJSON( "/api/clinics/?format=json&lat="+coords[0]+"&lon="+coords[1]+"&categories="+filterSel, function( data ) {
            console.log(data);



        });

    });
}

