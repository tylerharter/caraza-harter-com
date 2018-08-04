"use strict";

var common = {};

$(function() {
    var lambdaUrl = "https://1y4o8v9snh.execute-api.us-east-2.amazonaws.com/default/cs301"
    var googleToken = null
    var currQuestionId = null
    
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
	googleToken = null
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

    function callLambda(data, successFn, failureFn) {
	$.ajax({
	    type: "POST",
	    url: lambdaUrl,
	    data: JSON.stringify(data),
	    contentType: "application/json; charset=utf-8",
	    dataType: "json",
	    success: function(data) {
		console.log("post succeeded, got back %o", data)
		successFn(data)
	    },
	    failure: function(errMsg) {
		console.log("post failed")
		failureFn(errMsg)
	    }
	});
    }

    common.clickerSubmit = function(answer) {
	var data = {
	    "GoogleToken": googleToken,
	    "fn": "answer",
	    "question_id": currQuestionId,
	    "answer": answer
	}
	callLambda(data, function(data) {
	    // pass
	}, function(error) {
	    console.log(errMsg)
	})
    };

    common.clickerGetAnswers = function() {
	var data = {
	    "GoogleToken": googleToken,
	    "fn": "get_answers",
	}
	// TODO
    };

    common.clickerRefreshQuestion = function() {
	var data = {
	    "GoogleToken": googleToken,
	    "fn": "get_question"
	}
	callLambda(data, function(data) {
	    $("#question").val(data.body.question)
	    currQuestionId = data.body.id
	}, function(error) {
	    console.log(errMsg)
	})	
    };

    common.clickerUploadQuestion = function() {
	console.log($("#question").val())
	var data = {
	    "GoogleToken": googleToken,
	    "fn": "put_question",
	    "question": $("#question").val()
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
