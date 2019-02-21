"use strict";

(function() {
  function init() {
    common.signinCallback = function() {
      code_review.fetchStatus()
    }
  }

  code_review.fetchStatus = function() {
    var data = {
      "fn": "roster_entry"
    }

    common.callLambda(data, function(data) {
      console.log(data)
      $("#exam1").html(html)
    })
  };

  init()
})()
