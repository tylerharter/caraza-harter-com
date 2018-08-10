"use strict";

console.log("common.js loads")
var common = {};

(function() {
  common.signinCallback = null
  var lambdaUrl = "https://1y4o8v9snh.execute-api.us-east-2.amazonaws.com/default/cs301"
  var outstandingCalls = 0
  var googleProfile = null
  var googleAuth = null
  var authExpiresTimestamp = 0 // seconds

  function init() {
    console.log("common.js main()")
    console.log("gapiLoaded="+gapiLoaded)

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
    $("#thank_you").hide()

    // we don't know whether google has loaded yet.  If yes, use it
    // now.  If not, setup callback to use it later.
    if (gapiLoaded) {
      common.googleSignInRender()
    } else {
      gapiLoadedCallback = common.googleSignInRender
    }
  }

  common.googleSignInRender = function() {
    console.log('render signin')
    gapi.signin2.render('signin', {
      'scope': 'profile email',
      'width': 240,
      'height': 50,
      'longtitle': true,
      'theme': 'dark',
      'onsuccess': common.googleSignIn
    });
  }

  common.googleSignIn = function(googleUser) {
    googleProfile = googleUser.getBasicProfile();
    console.log("log on by " + googleProfile.getEmail() + " (" + googleProfile.getId() + ")");
    googleAuth = googleUser.getAuthResponse()
    console.log("token " + googleAuth.id_token + " expires in " + googleAuth.expires_in + " seconds");
    authExpiresTimestamp = Date.now()/1000 + googleAuth.expires_in

    $("#signin").hide()
    $("#signout").show()
    $("#useremail").text(googleProfile.getEmail() + " ")

    if (common.signinCallback != null) {
      common.signinCallback()
    }
  };

  common.googleSignOut = function() {
    googleProfile = null
    googleAuth = null
    authExpiresTimestamp = 0
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
    });

    $("#signin").show()
    $("#signout").hide()
    $("#useremail").text("")
  };

  common.getGoogleUserId = function() {
    if (googleProfile == null) {
      return null
    }
    return googleProfile.getId()
  }

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
    if (Date.now()/1000 > authExpiresTimestamp) {
      // this must run after the event handler looking for clicks to dismiss the error popup
      setTimeout(function() {
        $('#error_message').text("Session Expired.  Please refresh and sign in again (if necessary).")
        $('#error_box').show()
      }, 1)
      return
    }

    data["GoogleToken"] = googleAuth.id_token
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
    if ($(event.target).closest("#error_box").length == 0) {
      $('#error_box').hide()
    }
  });

  init()
})()
