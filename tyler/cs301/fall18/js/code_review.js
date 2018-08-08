"use strict";

var code_review = {};

$(function() {
  // code review object
  var cr = null

  function init() {
    $("#code_review_title").html("Code Review (" + common.getUrlParameter('project_id').toUpperCase() + ")")
    $("#code_viewer").html("")
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

  // this considers adding a higlight
  function codeMouseUp() {
    var s = window.getSelection()
    console.log(s)
    var node1 = findPyCodeChild(s.anchorNode)
    var node2 = findPyCodeChild(s.focusNode)
    if (node1 == null || node2 == null) {
      return
    }

    console.log(node1, node2)
    if (plainTextOffset(node1) > plainTextOffset(node2)) {
      var tmp = node1
      node1 = node2
      node2 = tmp
    }

    var filename = node1.parentElement.getAttribute("filename")  
    var offset = plainTextOffset(node1)
    var length = plainTextOffset(node2)+node2.textContent.length - offset

    for(var i=0; i<cr.highlights[filename].length; i++) {
      var highlight = cr.highlights[filename][i]
      if (!(offset+length <= highlight.offset || highlight.offset+highlight.length <= offset)) {
        // too close to another highlight (or overlapping)
        console.log('overlaps')
        return
      }
    }

    console.log('does not overlap')

    cr.highlights[filename].push({offset:offset, length:length})
    console.log(cr.highlights)
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

  function refreshHighlights() {
    if (Object.keys(cr.project.files).length == 0) {
      $("#code_viewer").html("no files found")
      return
    }
    
    var html = ''
    for (var filename in cr.project.files) {
      var code = cr.project.files[filename]

      // sort highlights from last to first.  Otherwise, injecting
      // HTML at specific offsets gets messed up, as early injections
      // move where later injections should go.
      cr.highlights[filename].sort(function(a, b){return b.offset-a.offset});

      // add all highlights
      for(var i=0; i<cr.highlights[filename].length; i++) {
        var highlight = cr.highlights[filename][i]
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

  code_review.fetchReview = function(force_new) {
    $("#code_viewer").html("")
    var project_id = $("#project_id").val()

    var data = {
      "fn": "get_code_review",
      "project_id": common.getUrlParameter('project_id'),
      "submitter_id": common.getUrlParameter('submitter_id'),
      "force_new": force_new
    }

    common.callLambda(data, function(data) {
      cr = data.body
      refreshHighlights()
    })
  };

  code_review.startFresh = function() {
    code_review.fetchReview(true)
  }

  code_review.saveCodeReview = function() {
    var new_cr = Object.assign({}, cr) // shallow copy
    new_cr.project = null // no reason to upload the code again

    var data = {
      "fn": "put_code_review",
      "project_id": common.getUrlParameter('project_id'),
      "submitter_id": common.getUrlParameter('submitter_id'),
      "cr": new_cr
    }

    common.callLambda(data, function(data) {
      common.popThankYou()
    })
  }

  init()
})
