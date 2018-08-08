"use strict";

var submission = {};

$(function() {
  var max_file_kb = 40 // 40KB
  // for upload package
  var filename = null
  var payload = null

  // dict of individual files
  var code_files = {}
  var highlights = {}

  function init() {
    $("#project_file").change(submission.openFile)

    //document.addEventListener("selectionchange", selectionChange);
  }

  // keep going up the DOM until we find the immediate child of a lang-py element
  function findPyCodeChild(node) {
    while(node.parentElement != null) {
      var classes = node.parentElement.classList
      if (classes != undefined && classes.contains("lang-py")) {
        break
      }
      node = node.parentElement
    }
    if (node.parentElement == null) {
      return null
    }
    return node
  }
  
  function plainTextOffset(node) {
    var offset = 0
    for (var i=0; i< node.parentElement.childNodes.length; i++) {
      var child = node.parentElement.childNodes[i]
      if (child == node) {
        return offset
      }
      offset += child.textContent.length
    }
    return offset
  }
  
  function codeMouseUp() {
    var s = window.getSelection()
    console.log(s)
    var node1 = findPyCodeChild(s.anchorNode)
    var node2 = findPyCodeChild(s.focusNode)
    if (node1 == null || node2 == null) {
      return
    }

    var filename = node1.parentElement.getAttribute("filename")
    console.log(node1, node2)
    var offset = plainTextOffset(node1)
    var length = plainTextOffset(node2)+node2.textContent.length - offset
    highlights[filename].push({offset:offset, length:length})
    console.log(highlights)
    refreshHighlights()
  }

  function addCodeReviewLink(code, offset, length) {
    var c = code.slice(0, offset)
    c += '<a href="#" class="code-review-link">'
    c += code.slice(offset, offset+length)
    c += '</a>'
    c += code.slice(offset+length)
    return c
  }

  submission.uploadCode = function() {
    var project = 'p0' // TODO

    var data = {
      "fn": "project_upload",
      "project": project,
      "filename": filename,
      "payload": payload
    }
    common.callLambda(data, function(data) {
      console.log("project uploaded")
      common.popThankYou()
    })
  };

  function refreshHighlights() {
    var html = ''
    for (var filename in code_files) {
      var code = code_files[filename]

      // add all highlights
      for(var i=0; i<highlights[filename].length; i++) {
        var highlight = highlights[filename][i]
        code = addCodeReviewLink(code, highlight.offset, highlight.length)
      }

      html += ('<h3>'+filename+'</h3>')
      html += ('<pre class="prettyprint lang-py" filename="'+filename+'">' +
               code +
               '</pre>')
    }
    $("#code_viewer").html(html)
    PR.prettyPrint()
    $(".prettyprint").mouseup(codeMouseUp)
  }
  
  submission.viewCode = function() {
    var project = 'p0' // TODO

    var data = {
      "fn": "project_view",
      "project": project,
    }
    common.callLambda(data, function(data) {
      console.log(data)
      code_files = {}
      for (var filename in data.body.files) {
        var code = data.body.files[filename]
        code_files[filename] = code
        highlights[filename] = []
      }

      refreshHighlights()
    })
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
})
