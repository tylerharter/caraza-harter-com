"use strict";

var code_review = {};

(function() {
  function init() {
    $("#summary").html("")

    common.signinCallback = function() {
      code_review.fetchSummary()
    }
  }

  code_review.fetchSummary = function() {
    var data = {
      "fn": "project_get_summary",
      "net_id": common.getUrlParameter('net_id'),
    }

    common.callLambda(data, function(data) {
      var html = "<h1>" + data.body.when + "</h1>\n"
      html += data.body.html_summary
      $("#summary").html(html)
    })
  };

  init()
})()
