/* Copyright Anthony J. Pesce and Jon Schleuss */

document.getElementById('find_locations').onclick=function(){
	console.log('find location');
	getLocation();
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