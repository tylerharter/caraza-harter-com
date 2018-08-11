"use strict";

var reviewer = {};

(function() {
  function init() {
    $("#project_id").change(reviewer.refresh_submissions)
  }

  reviewer.refresh_submissions = function() {
    console.log("refresh")
    $("submissions").val("")

    var data = {
      "fn": "project_list_submissions",
      "project_id": $("#project_id").val()
    }
    common.callLambda(data, function(data) {
      var submissions = data.body.submissions

      // break submissions into categories
      var categories = {}
      for (var i=0; i<submissions.length; i++) {
        var category = 'general'
        if (!(category in categories)) {
          categories[category] = []
        }
        categories[category].push(submissions[i])
      }

      // display links
      var body = $("#submissions")
      for (var category in categories) {
        $('<h3>',{
          text:category
        }).appendTo(body)

        for (var i=0; i<categories[category].length; i++) {
          var submission = categories[category][i]
          var url = ('code_review.html?project_id=' + submission.project_id +
                     '&submitter_id=' + submission.submitter_id)
          $('<a>',{
            text:'submitter='+submission.submitter_id,
            href:url,
            target:'_blank'
          }).appendTo(body)

          $('<br>').appendTo(body)
        }
      }
    })
  }

  init()
})()
