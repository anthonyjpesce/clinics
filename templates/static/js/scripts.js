/* Copyright Anthony J. Pesce and Jon Schleuss */

document.getElementById('find_locations').onclick=function(){
	console.log('find location');
	getLocation(); // get users location
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
$.getJSON( "{{ STATIC_URL }}/js/90029-50.json", function( data ) {
  var items = [];
  $.each( data, function( key, val ) {
    items.push( "<li id='" + key + "'>" + val + "</li>" );
  });
 
  $( "<ul/>", {
    "class": "my-new-list",
    html: items.join( "" )
  }).appendTo( "body" );
});