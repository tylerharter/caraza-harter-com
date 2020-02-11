var intl = require('../intl');

var Errors = require('../util/errors');
var GitCommands = require('../git/commands');
var MercurialCommands = require('../mercurial/commands');

var CommandProcessError = Errors.CommandProcessError;
var CommandResult = Errors.CommandResult;

var commandConfigs = {
  'git': GitCommands.commandConfig,
  'hg': MercurialCommands.commandConfig
};

var commands = {
  execute: function(vcs, name, engine, commandObj) {
    if (!commandConfigs[vcs][name]) {
      throw new Error('i don\'t have a command for ' + name);
    }
    var config = commandConfigs[vcs][name];
    if (config.delegate) {
      return this.delegateExecute(config, engine, commandObj);
    }

    config.execute.call(this, engine, commandObj);
  },

  delegateExecute: function(config, engine, commandObj) {
    // we have delegated to another vcs command, so lets
    // execute that and get the result
    var result = config.delegate.call(this, engine, commandObj);

    if (result.multiDelegate) {
      // we need to do multiple delegations with
      // a different command at each step
      result.multiDelegate.forEach(function(delConfig) {
        // copy command, and then set opts
        commandObj.setOptionsMap(delConfig.options || {});
        commandObj.setGeneralArgs(delConfig.args || []);

        commandConfigs[delConfig.vcs][delConfig.name].execute.call(this, engine, commandObj);
      }, this);
    } else {
      config = commandConfigs[result.vcs][result.name];
      // commandObj is PASSED BY REFERENCE
      // and modified in the function
      commandConfigs[result.vcs][result.name].execute.call(this, engine, commandObj);
    }
  },

  blankMap: function() {
    return {git: {}, hg: {}};
  },

  getShortcutMap: function() {
    var map = this.blankMap();
    this.loop(function(config, name, vcs) {
      if (!config.sc) {
        return;
      }
      map[vcs][name] = config.sc;
    }, this);
    return map;
  },

  getOptionMap: function() {
    var optionMap = this.blankMap();
    this.loop(function(config, name, vcs) {
      var displayName = config.displayName || name;
      var thisMap = {};
      // start all options off as disabled
      (config.options || []).forEach(function(option) {
        thisMap[option] = false;
      });
      optionMap[vcs][displayName] = thisMap;
    });
    return optionMap;
  },

  getRegexMap: function() {
    var map = this.blankMap();
    this.loop(function(config, name, vcs) {
      var displayName = config.displayName || name;
      map[vcs][displayName] = config.regex;
    });
    return map;
  },

  /**
   * which commands count for the git golf game
   */
  getCommandsThatCount: function() {
    var counted = this.blankMap();
    this.loop(function(config, name, vcs) {
      if (config.dontCountForGolf) {
        return;
      }
      counted[vcs][name] = config.regex;
    });
    return counted;
  },

  loop: function(callback, context) {
    Object.keys(commandConfigs).forEach(function(vcs) {
      var commandConfig = commandConfigs[vcs];
      Object.keys(commandConfig).forEach(function(name) {
        var config = commandConfig[name];
        callback(config, name, vcs);
      });
    });
  }
};

var parse = function(str) {
  var vcs;
  var method;
  var options;

  // see if we support this particular command
  var regexMap = commands.getRegexMap();
  Object.keys(regexMap).forEach(function (thisVCS) {
    var map = regexMap[thisVCS];
    Object.keys(map).forEach(function(thisMethod) {
      var regex = map[thisMethod];
      if (regex.exec(str)) {
        vcs = thisVCS;
        method = thisMethod;
        // every valid regex has to have the parts of
        // <vcs> <command> <stuff>
        // because there are always two space-groups
        // before our "stuff" we can simply
        // split on space-groups and grab everything after
        // the second:
        options = str.match(/('.*?'|".*?"|\S+)/g).slice(2);
      }
    });
  });

  if (!method) {
    return false;
  }

  // we support this command!
  // parse off the options and assemble the map / general args
  var parsedOptions = new CommandOptionParser(vcs, method, options);
  var error = parsedOptions.explodeAndSet();
  return {
    toSet: {
      generalArgs: parsedOptions.generalArgs,
      supportedMap: parsedOptions.supportedMap,
      error: error,
      vcs: vcs,
      method: method,
      options: options,
      eventName: 'processGitCommand'
    }
  };
};

/**
 * CommandOptionParser
 */
function CommandOptionParser(vcs, method, options) {
  this.vcs = vcs;
  this.method = method;
  this.rawOptions = options;

  this.supportedMap = commands.getOptionMap()[vcs][method];
  if (this.supportedMap === undefined) {
    throw new Error('No option map for ' + method);
  }

  this.generalArgs = [];
}

CommandOptionParser.prototype.explodeAndSet = function() {
  for (var i = 0; i < this.rawOptions.length; i++) {
    var part = this.rawOptions[i];

    if (part.slice(0,1) == '-') {
      // it's an option, check supportedMap
      if (this.supportedMap[part] === undefined) {
        return new CommandProcessError({
          msg: intl.str(
            'option-not-supported',
            { option: part }
          )
        });
      }

      var next = this.rawOptions[i + 1];
      var optionArgs = [];
      if (next && next.slice(0,1) !== '-') {
        // only store the next argument as this
        // option value if its not another option
        i++;
        optionArgs = [next];
      }
      this.supportedMap[part] = optionArgs;
    } else {
      // must be a general arg
      this.generalArgs.push(part);
    }
  }
};

exports.commands = commands;
exports.parse = parse;
