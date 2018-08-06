"use strict";

var common = {};

$(function() {
    var lambdaUrl = "https://1y4o8v9snh.execute-api.us-east-2.amazonaws.com/default/cs301"
    var outstandingCalls = 0
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

	$("#signout").hide()
	$('#error_box').hide()
    }

    common.googleSignOut = function() {
	googleToken = null
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signOut().then(function () {
	    console.log('User signed out.');
	});

	$("#signin").show()
	$("#signout").hide()
	$("#useremail").text("")
    };

    common.googleSignIn = function(googleUser) {
	// Useful data for your client-side scripts:
	var profile = googleUser.getBasicProfile();
	console.log("log on by " + profile.getEmail());
	googleToken = googleUser.getAuthResponse().id_token;

	$("#signin").hide()
	$("#signout").show()
	$("#useremail").text(profile.getEmail() + " ")

	common.clickerRefreshQuestion()
    };

    common.getUrlParameter = function(name) {
	name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
	var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
	var results = regex.exec(location.search);
	return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    };

    common.popError = function(msg) {
	$('#error_message').text(msg)
	$('#error_box').show()
    }

    common.callLambda = function(data, successFn, failureFn) {
	data["GoogleToken"] = googleToken
	outstandingCalls += 1
	console.log("outstanding calls=%d", outstandingCalls)
	$("#loader_wheel").show()

	function fail(error) {
	    console.log("post failed")
	    if (failureFn != null) {
		failureFn(error)
	    } else {
		common.popError(error)
	    }
	}

	$.post({
	    type: "POST",
	    url: lambdaUrl,
	    data: JSON.stringify(data),
	    contentType: "application/json; charset=utf-8",
	    dataType: "json"
	})
	    .done(function(data) {
		if (data.statusCode == 200) {
		    console.log("post succeeded, got back %o", data)
		    successFn(data)
		} else {
		    console.log("post returned status "+data.statusCode)
		    console.log("error body %o", data.body)
		    fail(data.body)
		}
	    })
	    .fail(function(error) {
		fail(error)
	    })
	    .always(function() {
		outstandingCalls -= 1
		console.log("outstanding calls=%d", outstandingCalls)
		if (outstandingCalls == 0) {
		    $("#loader_wheel").hide()
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
	    console.log("answer uploaded")
	})
    };

    common.clickerSummarizeAnswers = function() {
	var data = {
	    "GoogleToken": googleToken,
	    "fn": "get_answer_counts",
	}
	callLambda(data, function(data) {
	    var answers = data.body.answers
	    var total = 0
	    for(var k in answers) {
		total += answers[k]
	    }

	    var text = ""
	    Object.keys(answers).sort().forEach(function(k){
		var count = answers[k]
		text += (k + ": " + count + " (" + Math.round(count*100/total) + "%)\n")
	    })
	    $("#answers").val(text)

	    if (data.body.errors.length > 0) {
		console.log("Errors:")
		console.log(data.body.errors)
	    }
	})
    };

    common.clickerRefreshQuestion = function() {
	var data = {
	    "GoogleToken": googleToken,
	    "fn": "get_question"
	}
	callLambda(data, function(data) {
	    $("#question").val(data.body.question)
	    currQuestionId = data.body.id
	})
    };

    common.clickerUploadQuestion = function() {
	console.log($("#question").val())
	var data = {
	    "GoogleToken": googleToken,
	    "fn": "put_question",
	    "question": $("#question").val()
	}

	callLambda(data, function(data) {
	    console.log("question uploaded")
	})
    };

    main()
})
