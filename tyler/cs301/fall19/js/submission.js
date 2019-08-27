"use strict";

var submission = {};

(function() {
  var max_file_kb = 1024 // 1MB
  // for upload package
  var filename = null
  var payload = null

  function init() {
    $("#project_file").change(submission.openFile)
    $("#project_id").change(function() {
      $("#submission_status").html("")
    })
  }

  submission.uploadCode = function() {
    var project_id = $("#project_id").val()
    var ignore_errors = $("#ignore_errors").prop("checked")

    var data = {
      "fn": "project_upload",
      "project_id": project_id,
      "filename": filename,
      "payload": payload,
      "feedback_request": $("#feedback_request").val(),
      "ignore_errors":  ignore_errors
    }
    common.callLambda(data, function(data) {
      console.log("project uploaded")
      common.popThankYou()

      // try to preview right after a submission
      var analysis = data.body.analysis
      refreshProjectStatus(analysis)
      if (analysis.errors) {
        if (ignore_errors) {
          common.popError("your submission may not get graded (check bulleted errors carefully)")
        } else {
          common.popError("your submission was not uploaded due to errors (check bulleted errors carefully)")
        }
      }

      $("#project_file").val(null);
      $("#submit_button").prop('disabled', true)
    })
  };
  
  function refreshProjectStatus(analysis) {
    var html = '<h3>Submission Status</h3>'

    html += '<ul>'
    for (var i in analysis.comments) {
      var comment = analysis.comments[i]
      html += '<li>' + comment
    }
    html += '</ul>'

    $("#submission_status").html(html)
  }

  submission.viewCodeReview = function() {
    var student_email = common.getEmail() // submitted by self
    var project_id = $("#project_id").val()
    var url = "code_review.html?project_id="+project_id+"&student_email="+student_email
    window.open(url)
  };

  submission.openFile = function(event) {
    var reader = new FileReader();
    var file = event.target.files[0]

    reader.onload = function() {
      var b64contents = btoa(reader.result)
      filename = null
      payload = null

      if (file.name.endsWith('.py') || file.name.endsWith('.ipynb')) {
        if (reader.result.length <= max_file_kb*1024) {
          filename = file.name
          payload = b64contents
          $("#submit_button").prop('disabled', false)
        } else {
          common.popError("max file size is "+max_file_kb+"KB")
          $("#submit_button").prop('disabled', true)
        }
      } else {
        common.popError("only .py or .ipynb are accepted")
        $("#submit_button").prop('disabled', true)
      }
    };

    reader.readAsBinaryString(file)
  }

  init()
})()
