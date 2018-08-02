var common = {};

$(function() {
    function main() {
	// highlight current page
	var curr_page = window.location.pathname.split('/').slice(-1)[0]
	$('.nav-link').each(function(i,link) {
	    var curr_link = link.href.split('/').slice(-1)[0]

	    if (curr_link == curr_page) {
		$(link).parent().addClass("active")
	    }
	});
    }

    common.googleSignOut = function() {
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signOut().then(function () {
	    console.log('User signed out.');
	});
    }

    common.googleSignIn = function(googleUser) {
	// Useful data for your client-side scripts:
	var profile = googleUser.getBasicProfile();
	console.log("ID: " + profile.getId()); // Don't send this directly to your server!
	console.log('Full Name: ' + profile.getName());
	console.log('Given Name: ' + profile.getGivenName());
	console.log('Family Name: ' + profile.getFamilyName());
	console.log("Image URL: " + profile.getImageUrl());
	console.log("Email: " + profile.getEmail());
	
	// The ID token you need to pass to your backend:
	var id_token = googleUser.getAuthResponse().id_token;
	console.log("ID Token: " + id_token);
    };

    main()
})
