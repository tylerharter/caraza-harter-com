var common = {};

$(function() {
    var lambdaUrl = "https://1y4o8v9snh.execute-api.us-east-2.amazonaws.com/default/cs301"
    var googleToken = null
    
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
    };

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
	googleToken = googleUser.getAuthResponse().id_token;
	console.log("ID Token: " + googleToken);
    };

    common.clickerSubmit = function() {
	var data = {
	    "GoogleToken": googleToken,
	    "fn": "answer",
	    "question_id": "123",
	    "answer": "A"
	}

	$.ajax({
	    type: "POST",
	    url: lambdaUrl,
	    data: JSON.stringify(data),
	    contentType: "application/json; charset=utf-8",
	    dataType: "json",
	    success: function(data){
		console.log(data);
	    },
	    failure: function(errMsg) {
		console.log(errMsg);
	    }
	});
    };

    common.clickerGetAnswers = function() {
	var data = {
	    "GoogleToken": googleToken,
	    "fn": "get_answers",
	    "question_id": "123"
	}

	$.ajax({
	    type: "POST",
	    url: lambdaUrl,
	    data: JSON.stringify(data),
	    contentType: "application/json; charset=utf-8",
	    dataType: "json",
	    success: function(data){
		console.log(data);
	    },
	    failure: function(errMsg) {
		console.log(errMsg);
	    }
	});
    };

    main()
})
