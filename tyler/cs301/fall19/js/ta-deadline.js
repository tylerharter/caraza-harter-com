"use strict";

var ta_deadline = {};

(function() {
  function init() {
    $("#days").focus(function() {
      if ($("#days").val() == "") {
        ta_deadline.getExtension()
      }
    })

    $("#netid").on('input', function(){
      $("#days").val("")
    })

    $("#projectid").on('input', function(){
      $("#days").val("")
    })
  }

  ta_deadline.getExtension = function() {
    var project_id = $("#projectid").val()
    var net_id = $("#netid").val()

    var data = {
      "fn": "project_get_extension",
      "project_id": project_id,
      "net_id": net_id,
    }
    $("#days").val("...")
    common.callLambda(data, function(data) {
      $("#days").val(data.body.days)
    })
  };

  ta_deadline.setExtension = function() {
    var project_id = $("#projectid").val()
    var net_id = $("#netid").val()
    var days = $("#days").val()

    var data = {
      "fn": "project_set_extension",
      "project_id": project_id,
      "net_id": net_id,
      "days": days
    }
    common.callLambda(data, function(data) {
      common.popThankYou()
    })
  };

  init()
})()
