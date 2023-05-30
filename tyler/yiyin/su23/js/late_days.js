"use strict";

var status = {};

(function() {
  function getStudentEmail() {
    var email = common.getUrlParameter('student_email')
    if (!email) {
      email = common.getEmail()
    }
    return email
  }

  function init() {
    common.signinCallback = function() {
      var data = {
        "fn": "get_late_days",
        "topic": common.getUrlParameter('topic'),
        "student_email": getStudentEmail()
      }

      common.callLambda(data, function(data) {
        console.log(data)
        // $("#subject").html(data.body.subject)
        $("#late_days").html(data.body)
        // $("#rem_days").html(data.body.rem_days)
      })
    }
  }

  init()
})()
