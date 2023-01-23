var _ = require('underscore');
var Q = require('q');
var Backbone = require('backbone');
var marked = require('marked');

var util = require('../util');
var intl = require('../intl');
var KeyboardListener = require('../util/keyboard').KeyboardListener;
var Command = require('../models/commandModel').Command;

var ModalTerminal = require('../views').ModalTerminal;
var ContainedBase = require('../views').ContainedBase;

var Visualization = require('../visuals/visualization').Visualization;
var HeadlessGit = require('../git/headless');

var GitDemonstrationView = ContainedBase.extend({
  tagName: 'div',
  className: 'gitDemonstrationView box horizontal',
  template: _.template($('#git-demonstration-view').html()),

  events: {
    'click div.command > p.uiButton': 'positive'
  },

  initialize: function(options) {
    options = options || {};
    this.options = options;
    this.JSON = Object.assign(
      {
        beforeMarkdowns: [
          '## Git Commits',
          '',
          'Awesome!'
        ],
        command: 'git commit',
        afterMarkdowns: [
          'Now you have seen it in action',
          '',
          'Go ahead and try the level!'
        ]
      },
      options
    );

    var convert = function(markdowns) {
      return marked(markdowns.join('\n'));
    };

    this.JSON.beforeHTML = convert(this.JSON.beforeMarkdowns);
    this.JSON.afterHTML = convert(this.JSON.afterMarkdowns);

    this.container = new ModalTerminal({
      title: options.title || intl.str('git-demonstration-title')
    });
    this.render();
    this.checkScroll();

    this.navEvents = Object.assign({}, Backbone.Events);
    this.navEvents.on('positive', this.positive, this);
    this.navEvents.on('negative', this.negative, this);
    this.keyboardListener = new KeyboardListener({
      events: this.navEvents,
      aliasMap: {
        enter: 'positive',
        right: 'positive',
        left: 'negative'
      },
      wait: true
    });

    this.visFinished = false;
    this.initVis();

    if (!options.wait) {
      this.show();
    }
  },

  receiveMetaNav: function(navView, metaContainerView) {
    var _this = this;
    navView.navEvents.on('positive', this.positive, this);
    this.metaContainerView = metaContainerView;
  },

  checkScroll: function() {
    var children = this.$('div.demonstrationText').children().toArray();
    var heights = children.map(function(child) { return child.clientHeight; });
    var totalHeight = heights.reduce(function(a, b) { return a + b; });
    if (totalHeight < this.$('div.demonstrationText').height()) {
      this.$('div.demonstrationText').addClass('noLongText');
    }
  },

  dispatchBeforeCommand: function() {
    if (!this.options.beforeCommand) {
      return;
    }

    var whenHaveTree = Q.defer();
    HeadlessGit.getTreeQuick(this.options.beforeCommand, whenHaveTree);
    whenHaveTree.promise.then(function(tree) {
      this.mainVis.gitEngine.loadTree(tree);
      this.mainVis.gitVisuals.refreshTreeHarsh();
    }.bind(this));
  },

  takeControl: function() {
    this.hasControl = true;
    this.keyboardListener.listen();

    if (this.metaContainerView) { this.metaContainerView.lock(); }
  },

  releaseControl: function() {
    if (!this.hasControl) { return; }
    this.hasControl = false;
    this.keyboardListener.mute();

    if (this.metaContainerView) { this.metaContainerView.unlock(); }
  },

  reset: function() {
    this.mainVis.reset();
    this.dispatchBeforeCommand();
    this.demonstrated = false;
    this.$el.toggleClass('demonstrated', false);
    this.$el.toggleClass('demonstrating', false);
  },

  positive: function() {
    if (this.demonstrated || !this.hasControl) {
      // don't do anything if we are demonstrating, and if
      // we receive a meta nav event and we aren't listening,
      // then don't do anything either
      return;
    }
    this.demonstrated = true;
    this.demonstrate();
  },

  demonstrate: function() {
    this.$el.toggleClass('demonstrating', true);

    var whenDone = Q.defer();
    this.dispatchCommand(this.JSON.command, whenDone);
    whenDone.promise.then(function() {
      this.$el.toggleClass('demonstrating', false);
      this.$el.toggleClass('demonstrated', true);
      this.releaseControl();
    }.bind(this));
  },

  negative: function(e) {
    if (this.$el.hasClass('demonstrating')) {
      return;
    }
    this.keyboardListener.passEventBack(e);
  },

  dispatchCommand: function(value, whenDone) {
    var commands = [];
    util.splitTextCommand(value, function(commandStr) {
      commands.push(new Command({
        rawStr: commandStr
      }));
    }, this);

    var chainDeferred = Q.defer();
    var chainPromise = chainDeferred.promise;

    commands.forEach(function(command, index) {
      chainPromise = chainPromise.then(function() {
        var myDefer = Q.defer();
        this.mainVis.gitEngine.dispatch(command, myDefer);
        return myDefer.promise;
      }.bind(this));
      chainPromise = chainPromise.then(function() {
        return Q.delay(300);
      });
    }, this);

    chainPromise = chainPromise.then(function() {
      whenDone.resolve();
    });

    chainDeferred.resolve();
  },

  tearDown: function() {
    this.mainVis.tearDown();
    GitDemonstrationView.__super__.tearDown.apply(this);
  },

  hide: function() {
    this.releaseControl();
    this.reset();
    if (this.visFinished) {
      this.mainVis.setTreeIndex(-1);
      this.mainVis.setTreeOpacity(0);
    }

    this.shown = false;
    GitDemonstrationView.__super__.hide.apply(this);
  },

  show: function() {
    this.takeControl();
    if (this.visFinished) {
      setTimeout(function() {
        if (this.shown) {
          this.mainVis.setTreeIndex(300);
          this.mainVis.showHarsh();
        }
      }.bind(this), this.getAnimationTime() * 1.5);
    }

    this.shown = true;
    GitDemonstrationView.__super__.show.apply(this);
  },

  die: function() {
    if (!this.visFinished) { return; }

    GitDemonstrationView.__super__.die.apply(this);
  },

  initVis: function() {
    this.mainVis = new Visualization({
      el: this.$('div.visHolder div.visHolderInside')[0],
      noKeyboardInput: true,
      noClick: true,
      smallCanvas: true,
      zIndex: -1
    });
    this.mainVis.customEvents.on('paperReady', function() {
      this.visFinished = true;
      this.dispatchBeforeCommand();
      if (this.shown) {
        // show the canvas once its done if we are shown
        this.show();
      }
    }.bind(this));
  }
});

exports.GitDemonstrationView = GitDemonstrationView;
