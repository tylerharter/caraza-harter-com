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
    if (s.anchorNode == null || s.focusNode == null) {
      // these nodes are null when one clicks on a hyperlink
    }
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

    var filename = node1.parentElement.getAttribute("data-filename")
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

    cr.highlights[filename].push({offset:offset, length:length, comment:""})
    console.log(cr.highlights)
    refreshHighlights()
  }

  function getHighlightComment(filename, offset, length) {
    for(var i=0; i<cr.highlights[filename].length; i++) {
      var highlight = cr.highlights[filename][i]
      if (highlight.offset == offset && highlight.length == length) {
        return highlight.comment
      }
    }
    console.log("could not find highlight")
    return ""
  }

  function setHighlightComment(filename, offset, length, comment) {
    for(var i=0; i<cr.highlights[filename].length; i++) {
      var highlight = cr.highlights[filename][i]
      if (highlight.offset == offset && highlight.length == length) {
        highlight.comment = comment
        return
      }
    }
    console.log("could not find highlight")
  }

  function addCodeReviewLink(code, filename, offset, length) {
    var c = code.slice(0, offset)
    var span_id = ('highlight_'+offset+'_'+length)
    c += ('<span id="'+span_id+'" data-highlight-filename="'+filename+'" '+
          'data-highlight-offset="'+offset+'" data-highlight-length="'+length+'" '+
          'class="code-review-link" data-toggle="popover" data-placement="right" title="Comment">')
    c += code.slice(offset, offset+length)
    c += '</span>'
    c += code.slice(offset+length)
    return c
  }

  function refreshHighlights() {
    // remove all previous highlight popovers
    $(".popover").remove()

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
        code = addCodeReviewLink(code, filename, highlight.offset, highlight.length)
      }

      html += ('<h3>'+filename+'</h3>')
      html += ('<pre class="prettyprint lang-py" data-filename="'+filename+'">' +
               code +
               '</pre>')
    }

    $("#code_viewer").html(html)
    PR.prettyPrint()

    // for selection
    $(".prettyprint").mouseup(codeMouseUp)

    // must be after pretty printing
    $("[data-toggle=popover]").popover({html:true, container:"body"})
    $("[data-toggle=popover]").each(function() {
      var highlight_element = $(this)
      var highlight_id = $(this).attr('id')
      var offset = $(this).attr('data-highlight-offset')
      var length = $(this).attr('data-highlight-length')
      var filename = $(this).attr('data-highlight-filename')
      html = ('<textarea data-highlight-id="'+highlight_id+'" rows="5" cols="40"></textarea>' +
              '<br>' +
              '<button type="button" data-highlight-id="'+highlight_id+'" class="btn btn-dark" onclick="">OK</button>'
             )
      $(this).attr("data-content", html)

      // on show, register button events
      $(this).on('shown.bs.popover', function () {
        var txt = $("textarea[data-highlight-id="+highlight_id+"]")
        txt.val(getHighlightComment(filename, offset, length))

        var btn = $("button[data-highlight-id="+highlight_id+"]")
        btn.click(function() {
          highlight_element.popover('hide')
        })
      })

      // on close, persist results
      $(this).on('hide.bs.popover', function () {
        var txt = $("textarea[data-highlight-id="+highlight_id+"]")
        console.log(txt.val())
        setHighlightComment(filename, offset, length, txt.val())
      })
    })
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
