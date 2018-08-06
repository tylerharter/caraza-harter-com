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
    $("#loader_wheel").hide()
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

  common.popThankYou = function() {
    $("#thank_you").show()
    $("#thank_you").fadeOut(2000)
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

  // hide errors if click outside them 
  $(document).click(function(event) {
    if ($(event.target).closest(".alert").length == 0) {
      $('#error_box').hide()
    }
  });

  main()
})
