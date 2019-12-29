"use strict";

var status = {};

(function() {
  function init() {
    common.signinCallback = function() {
      var data = {
        "fn": "roster_entry"
      }

      common.callLambda(data, function(data) {
        console.log(data)
        $("#section").html(data.body.section)
        $("#ta_name").html(data.body.ta_name)
        $("#ta_email").html(data.body.ta_email)
      })
    }
  }

  init()
})()
