// Copyright 2018 Tyler Caraza-Harter
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

"use strict";

console.log("common.js loads")
var common = {};

(function() {
  common.signinCallback = null
  var lambdaUrl = "https://1y4o8v9snh.execute-api.us-east-2.amazonaws.com/default/cs301"
  var lambdaTestUrl = "https://5dthhwkgxl.execute-api.us-east-2.amazonaws.com/default/cs301"
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
      'onsuccess': common.googleSignIn,
      'prompt': 'select_account'
    });
  }

  common.googleSignIn = function(googleUser) {
    googleProfile = googleUser.getBasicProfile();
    console.log("log on by " + googleProfile.getEmail() + " (" + googleProfile.getId() + ")");
    googleAuth = googleUser.getAuthResponse()
    console.log("token " + googleAuth.id_token + " expires in " + googleAuth.expires_in + " seconds");
    common.googleToken = googleAuth.id_token;
    authExpiresTimestamp = Date.now()/1000 + googleAuth.expires_in

    $("#signin").hide()
    $("#signout").text(googleProfile.getEmail() + " Logout")
    $("#signout").show()
    $("#useremail").text(googleProfile.getEmail() + " ")

    if (common.signinCallback != null) {
      console.log("call signin callback")
      common.signinCallback()
    } else {
      console.log("no signin callback")
    }
  };

  common.googleSignOut = function() {
    googleProfile = null
    googleAuth = null
    authExpiresTimestamp = 0
    var auth2 = gapi.auth2.getAuthInstance();

    // show wait wheel while page refreshes
    auth2.signOut().then(function () {
      location.reload()
    });
  };

  common.getGoogleUserId = function() {
    if (googleProfile == null) {
      return null
    }
    return googleProfile.getId()
  }

  common.getEmail = function() {
    if (googleProfile == null) {
      return null
    }
    return googleProfile.getEmail()
  }

  common.getUrlParameter = function(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
  };

  common.popError = function(msg) {
    $('#error_message').html(msg.replace(/(?:\r\n|\r|\n)/g, '<br>'))
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

    var url = lambdaUrl
    if (common.getUrlParameter("lambda") == "test") {
      url = lambdaTestUrl
    }

    $.post({
      type: "POST",
      url: url,
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
