"use strict";

var code_review = {};

(function() {
  // code review object
  var cr = null
  var cr_dirty = false

  function init() {
    $("#code_review_title").html("Code Review (" + common.getUrlParameter('project_id').toUpperCase() + ")")
    $("#code_viewer").html("")

    var latest = common.getUrlParameter('latest')
    common.signinCallback = function() {code_review.fetchReview(latest == "1")}

    // prompt before leaving with unsaved work
    window.addEventListener("beforeunload", function (e) {
      if (cr_dirty) {
        var confirmationMessage = 'Leave without saving?';

        (e || window.event).returnValue = confirmationMessage; //Gecko + IE
        return confirmationMessage; //Gecko + Webkit, Safari, Chrome etc.
      }
    });
  }

  function nodeHasClass(node, cls) {
    var classes = node.classList
    return (classes != undefined && classes.contains(cls))
  }
  
  function findSelectionFileName(node) {
    while(node != null) {
      var classes = node.classList
      if (classes != undefined && classes.contains("lang-py")) {
        return node.getAttribute("data-filename")
      }
      node = node.parentElement
    }
    return null
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

  // get a plain text offset of selectionNode within an ancestor
  // element in the DOM marked with class rootClass
  function getAbsoluteOffset(selectionNode, selectionOffset, rootClass) {
    var node = selectionNode
    var offset = selectionOffset
    
    if (node == null) {
      return null
    }

    while(!nodeHasClass(node, rootClass) && node.parentElement != null) {
      offset += plainTextOffset(node)
      node = node.parentElement
    }

    if (!nodeHasClass(node, rootClass)) {
      // we never found the root element
      return null
    }

    return offset
  }

  // this considers adding a higlight
  function codeMouseUp() {
    if (cr == null || !cr.is_grader) {
      // students don't need to highlight
      return
    }

    var s = window.getSelection()
    var filename = findSelectionFileName(s.anchorNode)
    if (filename == null) {
      return
    }

    var offset1 = getAbsoluteOffset(s.anchorNode, s.anchorOffset, "lang-py")
    var offset2 = getAbsoluteOffset(s.focusNode, s.focusOffset, "lang-py")
    console.log(offset1)
    console.log(offset2)
    var offset = Math.min(offset1, offset2)
    var length = Math.max(offset1, offset2) - offset + 1

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
    cr_dirty = true
    console.log(cr.highlights)
    code_review.refreshCR()
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
        cr_dirty = true
        return
      }
    }
    console.log("could not find highlight")
  }

  function deleteHighlight(filename, offset, length) {
    for(var i=0; i<cr.highlights[filename].length; i++) {
      var highlight = cr.highlights[filename][i]
      if (highlight.offset == offset && highlight.length == length) {
        cr.highlights[filename].splice(i, 1) // delete at index i
        cr_dirty = true
        return
      }
    }
    console.log("could not find highlight")
  }

  function escapeForHTML(s) {
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }
  
  function getCodeReviewSpan(filename, offset, length) {
    var span_id = ('highlight_'+offset+'_'+length)
    return ('<span id="'+span_id+'" data-highlight-filename="'+filename+'" '+
            'data-highlight-offset="'+offset+'" data-highlight-length="'+length+'" '+
            'class="code-review-link" data-toggle="popover" data-placement="right" title="Comment">')
  }

  function fileConf(filename) {
    if ('files_meta' in cr.project && filename in cr.project.files_meta) {
      return cr.project.files_meta[filename]
    }

    // default
    return {display_name:filename, order:0, content_type:"python"}
  }

  code_review.genericComment = function(comment) {
    $("#general_comments").val(comment);
    cr.general_comments = comment;
  }

  code_review.resetVisible = function () {
    if (cr.is_grader) {
      $(".grader_content").show()
    } else {
      $(".grader_content").hide()
    }
  }

  code_review.refreshCR = function() {
    code_review.resetVisible()

    // remove all previous highlight popovers
    $(".popover").remove()

    if (Object.keys(cr.project.files).length == 0) {
      $("#code_viewer").html("no files found")
      return
    }

    var html = ''

    if ('test_result' in cr && cr.test_result != null && 'score' in cr.test_result) {
      $("#auto_test_score").val(cr.test_result.score)
    } else {
      $("#auto_test_score").val("not ready")
    }

    // check deductions
    var ta_deduction = 0
    if ('points_deducted' in cr) {
      ta_deduction = cr.points_deducted
    }
    $("#ta_point_deduction").val(ta_deduction)
    $("#ta_point_deduction").on('input', function(){
      var deduction = NaN
      var deduction_str = $("#ta_point_deduction").val()
      if (/^\d+$/.test(deduction_str)) {
        deduction = parseInt(deduction_str)
      }

      if (deduction != NaN && deduction >= 0 && deduction <= 100) {
        cr.points_deducted = deduction
        $("#ta_point_deduction").removeClass('is-invalid')
      } else {
        $("#ta_point_deduction").addClass('is-invalid')
      }
    })

    // show reviewer info, and grading info (if ready)
    if ('reviewer_email' in cr && cr.reviewer_email) {
      html += ('<p my="3">Reviewer: '+cr.reviewer_email+'</p>')

      // do we have a test score?
      if ('test_result' in cr && cr.test_result != null && 'score' in cr.test_result) {
        var test_score = cr.test_result.score
        var final_score = (test_score - ta_deduction)
        html += ('<ul>')
        html += ('<li>Base score: ' + test_score + ' (from tests)')
        html += ('<li>Less ' + ta_deduction + ' points (TA deduction)')
        html += ('<li>Final score: <b>' + final_score + '</b>')
        html += ('<li>Note: this final score does not consider whether this project was ' +
                 'submitted late.  If it was, and you did not have late days left, ' +
                 'you may not receive all these points.')
        if (final_score != 100) {
          html += ('<li>' + "Not the score you were expecting?  Don't panic.  " +
                   "Reach out to your reviewer to understand what went wrong.  " +
                   "Please copy the URL of this page to the email you send them.  " +
                   "If something trivial (e.g., wrong file name or missing comment " +
                   "about your partner) caused you to get zero, we'll be reasonable and " +
                   "help you fix it.")
        }
        html += ('</ul>')
      }
    }

    // show general comments
    var general_comments = ''
    if ('general_comments' in cr && cr.general_comments) {
      general_comments = cr.general_comments
    }
    html += ('<h3>General Comments</h3>')
    html += ('<textarea cols=80 rows=6 id="general_comments">'+general_comments+'</textarea><br>')
    html += ('<div class="grader_content" style="display:none;">')
    html += ('<button type="button" class="btn btn-dark" onclick="code_review.genericComment(\'Great job!\')">Great job!</button> ')
    html += ('<button type="button" class="btn btn-dark" onclick="code_review.genericComment(\'Good job!\')">Good job!</button> ')
    html += ('<button type="button" class="btn btn-dark" onclick="code_review.genericComment(\'Good job!  Please check comments below.\')">Good job! Please check comments below.</button> ')
    html += ('</div>')

    // create a box for each code file
    for (var filename in cr.project.files) {
      html += ('<h4 class="mt-3">'+fileConf(filename).display_name+'</h4>')
      html += ('<div class=html_code data-filename="'+filename+'">')
      html += ('<pre class="prettyprint lang-py" data-filename="'+filename+'"></pre>')
      html += ('</div>')
    }
    $("#code_viewer").html(html)
    code_review.resetVisible()

    // populate each box with the code and highlights
    for (var filename in cr.project.files) {
      // populate either the outer div with HTML content or the inner
      // pre (depending on the type of content
      if (fileConf(filename).content_type == "html") {
        var element = $("div[data-filename='"+filename+"'].html_code")
        element.html('<div class="nb_cell">' +
                     cr.project.files[filename] + 
                     '</div>')
      } else {
        var preElement = $("pre[data-filename='"+filename+"'].lang-py")
        var code = cr.project.files[filename]

        // sort highlights from last to first.  Otherwise, injecting
        // HTML at specific offsets gets messed up, as early injections
        // move where later injections should go.
        cr.highlights[filename].sort(function(a, b){return b.offset-a.offset});

        var htmlCode = ''

        // add all highlights
        for(var i=0; i<cr.highlights[filename].length; i++) {
          var highlight = cr.highlights[filename][i]
          var cut

          // move tail from code to htmlCode
          cut = highlight.offset + highlight.length
          htmlCode = escapeForHTML(code.slice(cut)) + htmlCode
          code = code.slice(0, cut)

          // move highlight from code to htmlCode
          cut = highlight.offset
          var span = getCodeReviewSpan(filename, highlight.offset, highlight.length)
          htmlCode = span + escapeForHTML(code.slice(cut)) + '</span>' + htmlCode
          code = code.slice(0, cut)
        }
        htmlCode = escapeForHTML(code) + htmlCode
        preElement.html(htmlCode)
      }
    }

    // add syntax coloring and watch for events
    PR.prettyPrint()
    $(".prettyprint").mouseup(codeMouseUp)

    // general comment update event
    if (cr.is_grader) {
      $("#general_comments").on('input', function(){
        cr.general_comments = $("#general_comments").val()
      })
    } else {
      $("#general_comments").prop( "disabled", true );
    }

    // must be after pretty printing
    $("[data-toggle=popover]").popover({html:true, container:"body"})
    $("[data-toggle=popover]").each(function() {
      var highlight_element = $(this)
      var highlight_id = $(this).attr('id')
      var offset = $(this).attr('data-highlight-offset')
      var length = $(this).attr('data-highlight-length')
      var filename = $(this).attr('data-highlight-filename')
      var readonly = cr.is_grader ? "" : "readonly"
      html = ('<textarea data-highlight-id="'+highlight_id+'" rows="5" cols="40" '+readonly+'></textarea>' +
              '<br>' +
              '<button type="button" data-highlight-id="'+highlight_id+'" data-highlight-button="ok" class="btn btn-dark">OK</button>'
             )
      if (cr.is_grader) {
        html += (' <button type="button" data-highlight-id="' + highlight_id +
                 '"data-highlight-button="cancel" class="btn btn-dark">Cancel</button>')
        html += (' <button type="button" data-highlight-id="' + highlight_id +
                 '"data-highlight-button="delete" class="btn btn-dark">Delete</button>')
      }
      $(this).attr("data-content", html)

      // on show, register button events
      $(this).on('shown.bs.popover', function () {
        var txt = $("textarea[data-highlight-id="+highlight_id+"]")
        var ok_btn = $("button[data-highlight-id="+highlight_id+"][data-highlight-button=ok]")
        var delete_btn = $("button[data-highlight-id="+highlight_id+"][data-highlight-button=delete]")
        var cancel_btn = $("button[data-highlight-id="+highlight_id+"][data-highlight-button=cancel]")

        txt.val(getHighlightComment(filename, offset, length))

        ok_btn.click(function() {
          if (cr.is_grader) {
            setHighlightComment(filename, offset, length, txt.val())
          }
          highlight_element.popover('hide')
        })

        cancel_btn.click(function() {
          code_review.refreshCR()
          highlight_element.popover('hide')
        })

        delete_btn.click(function() {
          deleteHighlight(filename, offset, length)
          code_review.refreshCR()
        })
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
      code_review.refreshCR()
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
      cr_dirty = false
      common.popThankYou()
      code_review.refreshCR()
    })
  }

  init()
})()
