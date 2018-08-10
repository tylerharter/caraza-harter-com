"use strict";

var submission = {};

(function() {
  var max_file_kb = 40 // 40KB
  // for upload package
  var filename = null
  var payload = null

  // code review object
  var cr = null

  function init() {
    $("#project_file").change(submission.openFile)
    $("#project_id").change(function() {
      $("#code_viewer").html("")
    })
  }

  submission.uploadCode = function() {
    var project_id = $("#project_id").val()

    var data = {
      "fn": "project_upload",
      "project_id": project_id,
      "filename": filename,
      "payload": payload
    }
    common.callLambda(data, function(data) {
      console.log("project uploaded")
      common.popThankYou()
    })
  };

  function refreshPreview() {
    if (Object.keys(cr.project.files).length == 0) {
      $("#code_viewer").html("no files found")
      return
    }
    
    var html = ''
    for (var filename in cr.project.files) {
      var code = cr.project.files[filename]

      html += ('<h3>'+filename+'</h3>')
      html += ('<pre class="prettyprint lang-py" filename="'+filename+'">' +
               code +
               '</pre>')
    }
    $("#code_viewer").html(html)
    PR.prettyPrint()
  }
  
  submission.viewCode = function() {
    var project_id = $("#project_id").val()

    // we fetch the code as a CR, even though we don't display
    // highlights.  We also do force_new to get latest code (not
    // previous code that may have already been reviewed).
    var data = {
      "fn": "get_code_review",
      "project_id": project_id,
      "submitter_id": null,
      "force_new": true
    }
    common.callLambda(data, function(data) {
      cr = data.body
      refreshPreview()
    })
  };

  submission.viewCodeReview = function() {
    var submitter_id = common.getGoogleUserId() // submitted by self
    var project_id = $("#project_id").val()
    var url = "code_review.html?project_id="+project_id+"&submitter_id="+submitter_id
    window.open(url)
  };

  submission.openFile = function(event) {
    var reader = new FileReader();
    var file = event.target.files[0]

    reader.onload = function() {
      var b64contents = btoa(reader.result)
      filename = null
      payload = null

      if (file.name.endsWith('.zip') || file.name.endsWith('.py')) {
        if (reader.result.length <= max_file_kb*1024) {
          filename = file.name
          payload = b64contents
          $("#submit_button").prop('disabled', false)
        } else {
          common.popError("max file size is "+max_file_kb+"KB")
          $("#submit_button").prop('disabled', true)
        }
      } else {
        common.popError("only .py or .zip are accepted")
        $("#submit_button").prop('disabled', true)
      }
    };

    reader.readAsBinaryString(file)
  }

  init()
})()
