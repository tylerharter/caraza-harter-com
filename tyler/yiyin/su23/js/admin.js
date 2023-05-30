"use strict";

var admin = {};

(function() {
  function init() {
    // pass
  }

  admin.get_roster = function() {
    var data = {
      "fn": "get_roster"
    }
    common.callLambda(data, function(data) {
      $("#roster").val(data.body.roster)
      $("#put_roster").prop('disabled', false);
    })
  };

  admin.put_roster = function() {
    var data = {
      "fn": "put_roster",
      "roster": $("#roster").val()
    }
    common.callLambda(data, function(data) {
      common.popThankYou()
    })
  };

  admin.gen_link_codes = function(overwrite_existing) {
    var data = {
      "fn": "roster_gen_link_codes",
      "overwrite_existing": overwrite_existing
    }
    common.callLambda(data, function(data) {
      $("#roster").val(data.body.roster)
    })
  };

  admin.merge_google_ids = function() {
    var data = {
      "fn": "roster_merge_google_ids",
    }
    common.callLambda(data, function(data) {
      $("#roster").val(data.body.roster)
    })
  }

  init()
})()
