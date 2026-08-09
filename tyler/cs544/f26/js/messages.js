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
        "fn": "get_message",
        "topic": common.getUrlParameter('topic'),
        "student_email": getStudentEmail()
      }

      common.callLambda(data, function(data) {
        console.log(data)
        $("#subject").html(data.body.subject)
        $("#msg").html(data.body.msg)
      })
    }
  }

  init()
})()
