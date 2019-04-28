"use strict";

var code_review = {};

var thumb_up_img = '<svg viewBox="0 0 200 200"><path stroke="#FFFFFF" stroke-width="9" stroke-miterlimit="10" d="m112.37 4.544s-6.518-0.448-8.766 6.069-2.02 16.407-2.02 16.407-7.191 14.834-15.058 20.678-20.677 12.585-20.677 12.585-2.696 2.248-4.046 5.395c-1.349 3.146-7.416 20.902-7.416 20.902s-4.496 11.014-11.463 18.43c-6.968 7.417-10.339 8.991-14.16 10.114-3.82 1.123-5.169 2.248-5.169 2.248l7.192 76.866s15.732-7.866 21.576-6.743 15.059 1.123 22.026 4.72c6.967 3.597 43.377 4.943 62.481-2.697s23.6-3.371 27.87-13.935-6.745-11.014-7.418-14.834 11.238-3.371 12.812-11.912c0.529-2.873-3.438-9.617-10.113-14.384-3.147-2.248 13.26 0.674 11.687-14.609-0.734-7.144-2.698-8.765-9.44-10.563-6.741-1.798 11.014-4.495 10.114-15.284-0.611-7.336-10.548-14.668-26.071-15.732-16.406-1.123-24.947-0.898-24.947-0.898l-17.081-1.124s11.463-18.654 15.732-25.397c4.27-6.742 9.663-21.801 9.214-24.947-0.44-3.158-1.12-23.162-16.85-21.364z" fill="#222222"/></svg>'

var thumb_down_img = '<svg viewBox="0 0 200 200"><path stroke="#FFFFFF" stroke-width="9" stroke-miterlimit="10" d="m112.37 194.98s-6.518 0.448-8.766-6.069-2.023-16.406-2.023-16.406-7.191-14.834-15.058-20.678-20.678-12.586-20.678-12.586-2.696-2.248-4.046-5.395c-1.349-3.146-7.416-20.902-7.416-20.902s-4.496-11.014-11.463-18.43c-6.968-7.417-10.339-8.991-14.16-10.114-3.82-1.123-5.169-2.248-5.169-2.248l7.192-76.866s15.732 7.866 21.576 6.743 15.059-1.123 22.026-4.72c6.967-3.597 43.377-4.943 62.481 2.697s23.6 3.371 27.87 13.935-6.745 11.014-7.418 14.834 11.238 3.371 12.812 11.912c0.529 2.873-3.438 9.617-10.113 14.384-3.147 2.248 13.26-0.674 11.687 14.609-0.734 7.144-2.698 8.765-9.44 10.563-6.741 1.798 11.014 4.495 10.114 15.284-0.611 7.336-10.548 14.668-26.071 15.732-16.406 1.123-24.947 0.898-24.947 0.898l-17.081 1.124s11.463 18.654 15.732 25.397c4.27 6.742 9.663 21.801 9.214 24.947-0.43 3.16-1.11 23.16-16.84 21.36z" fill="#222222"/></svg>'

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

  function setHighlightRating(filename, offset, length, rating) {
    for(var i=0; i<cr.highlights[filename].length; i++) {
      var highlight = cr.highlights[filename][i]
      if (highlight.offset == offset && highlight.length == length) {
        highlight.rating = rating
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

    // SECTION: grades (tests - ta deduction, only shown when both are ready)
    html += ('<h3>Grades</h3>')
    
    var grades_are_ready = ('reviewer_email' in cr && cr.reviewer_email &&
                            'test_result' in cr && cr.test_result != null &&
                            'score' in cr.test_result)
    
    if (grades_are_ready) {
      var test_score = cr.test_result.score
      var final_score = (test_score - ta_deduction)

      html += ('<ul>')
      html += ('<li>Base score: ' + test_score + ' (from tests)')
      html += ('<li>Less ' + ta_deduction + ' points (TA deduction)')
      html += ('<li>Final score: <b>' + final_score + '</b>')
      html += ('<li>Reviewer Contact Email: ' + cr.reviewer_email)
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
    } else {
      html += ('<p>not ready</p>')
    }

    // SECTION: test results
    html += ('<h3>Test Results</h3>')
    var test_blob = ""
    if ('test_result' in cr && cr.test_result != null && 'score' in cr.test_result) {
      $("#auto_test_score").val(cr.test_result.score)
      html += ('<textarea cols=80 rows=6 id="test_blob"></textarea><br>')
      test_blob = JSON.stringify(cr.test_result, null, 2)
    } else {
      html += ('<p>not ready</p>')
    }

    // SECTION: TA comments
    html += ('<h3>General Reviever Comments</h3>')
    var general_comments = ''
    if ('general_comments' in cr && cr.general_comments) {
      general_comments = cr.general_comments
    }
    html += ('<textarea cols=80 rows=6 id="general_comments">'+general_comments+'</textarea><br>')
    html += ('<div class="grader_content" style="display:none;">')
    html += ('<button type="button" class="btn btn-dark" onclick="code_review.genericComment(\'Great job!\')">Great job!</button> ')
    html += ('<button type="button" class="btn btn-dark" onclick="code_review.genericComment(\'Good job!\')">Good job!</button> ')
    html += ('<button type="button" class="btn btn-dark" onclick="code_review.genericComment(\'Good job!  Please check comments below.\')">Good job! Please check comments below.</button> ')
    html += ('</div>')

    // SECTION: rating the CR
    if (common.getUrlParameter("ratings") == "1") {
      if (grades_are_ready && !cr.is_grader) {
        html += ('<h3>Was Our Feedback Useful?</h3>')
        html += ('<ol>')
        html += ('<li>Click any yellow highlights below to view our feedback on specific lines of code')
        html += ('<li>Mark each comment we left you as useful (thumbs up) or not useful (thumbs down)')
        html += ('<li>Write a sentence or two about what you think could most be improved in your code if you were to do this project again (either based on our feedback or your own self critique)')
        html += ('<li>Click "Submit Response" to share your thoughts with us (counts for participation)')
        html += ('<ol>')
        html += ('<textarea cols=80 rows=6 id="cr_response"></textarea><br>')
        html += ('<button type="button" class="btn btn-dark")">Submit Response</button>')
      }
    }

    // SECTION: cells/files

    // create a box for each code file
    for (var filename in cr.project.files) {
      html += ('<h4 class="mt-3">'+fileConf(filename).display_name+'</h4>')
      html += ('<div class=html_code data-filename="'+filename+'">')
      html += ('<pre class="prettyprint lang-py" data-filename="'+filename+'"></pre>')
      html += ('</div>')
    }

    // LOAD HTML to PAGE
    $("#code_viewer").html(html)
    $("#test_blob").val(test_blob)
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
      $("#general_comments").prop("disabled", true);
    }

    // must be after pretty printing
    $("[data-toggle=popover]").popover({html:true, container:"body"})
    $("[data-toggle=popover]").each(function() {
      var highlight_element = $(this)
      var highlight_id = $(this).attr('id')
      var offset = $(this).attr('data-highlight-offset')
      var length = $(this).attr('data-highlight-length')
      var filename = $(this).attr('data-highlight-filename')
      var text_opts = cr.is_grader ? "" : "readonly"
      html = '<textarea data-highlight-id="'+highlight_id+'" rows="5" cols="40" '+text_opts+'></textarea><br>'

      // everybody buttons: Cancel, Delete
      html += ('<button type="button" data-highlight-id="' + highlight_id +
               '" data-highlight-button="ok" class="btn btn-dark">OK</button> ')

      if (cr.is_grader) {
        // grader buttons: Cancel, Delete
        html += ('<button type="button" data-highlight-id="' + highlight_id +
                 '"data-highlight-button="cancel" class="btn btn-dark">Cancel</button> ')
        html += ('<button type="button" data-highlight-id="' + highlight_id +
                 '"data-highlight-button="delete" class="btn btn-dark">Delete</button> ')
      } else {
        // student buttons: thumbs up, thumbs down
        var extra = 'class="btn btn-dark" style="width:50px;height:50px"'
        html += ('<button type="button" data-highlight-id="' + highlight_id +
                 '" data-highlight-button="down" '+extra+'>' + thumb_down_img + '</button> ')
        html += ('<button type="button" data-highlight-id="' + highlight_id +
                 '" data-highlight-button="up" '+extra+'>' + thumb_up_img + '</button> ')
      }
      $(this).attr("data-content", html)

      // on show, register button events
      $(this).on('shown.bs.popover', function () {
        var txt = $("textarea[data-highlight-id="+highlight_id+"]")
        var ok_btn = $("button[data-highlight-id="+highlight_id+"][data-highlight-button=ok]")
        var down_btn = $("button[data-highlight-id="+highlight_id+"][data-highlight-button=down]")
        var up_btn = $("button[data-highlight-id="+highlight_id+"][data-highlight-button=up]")
        var delete_btn = $("button[data-highlight-id="+highlight_id+"][data-highlight-button=delete]")
        var cancel_btn = $("button[data-highlight-id="+highlight_id+"][data-highlight-button=cancel]")

        txt.val(getHighlightComment(filename, offset, length))

        ok_btn.click(function() {
          if (cr.is_grader) {
            setHighlightComment(filename, offset, length, txt.val())
          }
          highlight_element.popover('hide')
        })

        up_btn.click(function() {
          highlight_element.popover('hide')
          setHighlightRating(filename, offset, length, "good")
        })

        down_btn.click(function() {
          highlight_element.popover('hide')
          setHighlightRating(filename, offset, length, "bad")
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

  code_review.rateCodeReview = function() {
    var rated_cr = Object.assign({}, cr) // shallow copy
    rated_cr.project = null // no reason to upload the code again

    var data = {
      "fn": "rate_code_review",
      "project_id": common.getUrlParameter('project_id'),
      "submitter_id": common.getUrlParameter('submitter_id'),
      "cr": rated_cr
    }

    common.callLambda(data, function(data) {
      cr_dirty = false
      common.popThankYou()
      code_review.refreshCR()
    })
  }

  init()
})()
