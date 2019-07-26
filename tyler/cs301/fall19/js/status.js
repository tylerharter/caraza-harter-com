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
        $("#exam1").html(data.body.exam1)
        $("#exam2").html(data.body.exam2)
        $("#final").html(data.body.final)
      })
    }
  }

  init()
})()
