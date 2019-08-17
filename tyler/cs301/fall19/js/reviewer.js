"use strict";

var reviewer = {};

(function() {
  function init() {
    $("#project_id").change(reviewer.refresh_submissions)

    var btn = document.querySelector('button#copyGoogleToken');
    btn.hidden = false;
    btn.addEventListener('click', reviewer.copy_google_token_to_clipboard);
  }

  reviewer.copy_google_token_to_clipboard = function() {
      var textarea = document.createElement('textarea');
      textarea.value = common.googleToken;

      // hide the textarea and copy to clipboard
      textarea.setAttribute('readonly', '');
      textarea.style.position = 'absolute';
      textarea.style.left = '-9999px';
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
  }

  reviewer.refresh_submissions = function() {
    console.log("refresh")
    $("#submissions").empty()

    if ($("#project_id").val() == "") {
      return
    }

    var data = {
      "fn": "project_list_submissions",
      "project_id": $("#project_id").val()
    }
    common.callLambda(data, function(data) {
      var submissions = data.body.submissions

      // break submissions into categories
      var categories = {}
      for (var i=0; i<submissions.length; i++) {
        var submission = submissions[i]
        var display = submission.submitter_id
        var category = 'Misc'
        if (submission.info.net_id != null) {
          display = submission.info.net_id
          category = 'Students'
        }
        if (submission.info.ta != null) {
          category = submission.info.ta
        }

        if (!(category in categories)) {
          categories[category] = []
        }

        submissions[i].display = display
        if (submissions[i].has_review) {
          submissions[i].display += ' [REVIEWED]'
        }
        categories[category].push(submission)
      }

      // display links
      var body = $("#submissions")

      $('<h1>',{
          text: 'Sumbissions: ' + submissions.length
      }).appendTo(body)

      for (var category in categories) {
        var student_count = categories[category].length
        $('<h3>',{
          text: category + '(' + student_count + ')'
        }).appendTo(body)

        for (var i=0; i<student_count; i++) {
          var submission = categories[category][i]
          var url = ('code_review.html?project_id=' + submission.project_id +
                     '&student_email=' + submission.student_email +
                     '&submission_id=' + submission.submission_id)

          $('<a>',{
            text:submission.display,
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
