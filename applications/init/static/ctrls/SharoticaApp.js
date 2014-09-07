
var sharoticaApp = angular.module('sharoticaApp', []);

sharoticaApp.controller('sideBarMenuCtrl',
	[        "$scope", "$http", "sharoticaService", "LocalStorage", "$rootScope",
	function ($scope,   $http,   sharoticaService,   LocalStorage,   $rootScope) {

	var sharoticaStorage = new LocalStorage("shar");
	$scope.innerCircleList = [];
	$scope.goodFriendsList = [];
	$scope.friendList = [];
	$scope.publicList = [];
	$scope.blockedList = [];
	$scope.unReadMessageCount = '';
	getBasicData();
	getNewMessageCount();

	function getNewMessageCount() {
		sharoticaService.getNewMessageCount().then(function(data) {
			$scope.unReadMessageCount = data.count;
		});
	}

	function getBasicData() {
		var tempHolder = sharoticaStorage.getObject($rootScope.accountKey + '_basic');
		if (tempHolder) {
			$rootScope.basicData = tempHolder;
			setFriendsList();
		} else {
			sharoticaService.getBasicData().then(function(data) {
			$rootScope.basicData = data;
			sharoticaStorage.set($rootScope.accountKey + '_basic', $rootScope.basicData);
			setFriendsList();
			});
		}
	}

	function setFriendsList () {
		angular.forEach($rootScope.basicData.friends, function(friend){
			if (friend.viewLevel == 2){
				$scope.innerCircleList.push(friend);
			} else if (friend.viewLevel == 3){
				$scope.goodFriendsList.push(friend);
			} else if (friend.viewLevel == 4){
				$scope.friendList.push(friend);
			} else if (friend.viewLevel == 5){
				$scope.publicList.push(friend);
			} else if (friend.viewLevel == 6){
				$scope.blockedList.push(friend);
			}
		});
	}
}]);

sharoticaApp.controller('topBarMenuCtrl',
	[        "$scope", "$http", "sharoticaService", "$rootScope",
	function ($scope,   $http,   sharoticaService,   $rootScope) {

	$scope.unReadMessages = '';
	getNewMessages();

	$scope.getMessage = function (messageKey) {
		window.location = "/init/messages/index?message_id=" + messageKey;
	}

	function getNewMessages() {
		sharoticaService.getNewMessages().then(function(data) {
			$scope.unReadMessages = data.messages;
			setTimeDelta();
		});
	}

	function setTimeDelta() {
		var currentTime = new Date().getTime();
		angular.forEach($scope.unReadMessages, function(message){
			var tempDate = Date.parse(message.whenSent);
			var deltaTime = currentTime - tempDate;
			if (deltaTime <= 3600000) {
				message.time = (deltaTime / 60000).toFixed(0) + ' minutes ago';
			} else if (deltaTime <= 86400000) {
				message.time = (deltaTime / 3600000).toFixed(0) + ' hours ago';
			} else if (deltaTime <= 604800000) {
				message.time = (deltaTime / 86400000).toFixed(0) + ' days ago';
			} else if (deltaTime <= 2419200000) {
				message.time = (deltaTime / 604800000).toFixed(0) + ' weeks ago';
			} else {
				message.time = 'cade';
			}
        });
	}
}]);

sharoticaApp.factory("sharoticaService",
	[       "$q", "$http",
	function($q,   $http) {

	return {
		getBasicData: function() {
			return $http.get('/init/api_shar/basic_data.json').then(function (response) {
				return response.data.basicData;
			});
		},
		getNewMessages: function() {
			return $http.get('/init/api_shar/new_messages.json').then(function (response) {
				return response.data;
			});
		},
		getNewMessageCount: function() {
			return $http.get('/init/api_shar/message_count.json').then(function (response) {
				return response.data;
			});
		},
		likeMedia: function(likeType, mediaID) {
			return $http.get('/init/api_shar/like_media.json?media_id='+mediaID+'&l_type='+likeType).then(function (response) {
				return response.data;
			});
		}
	};

}]);


//
// Slim wrapper for the browser's localStorage functionality.  The main additional functionality
// added by this class is the following:
//      1. Configurable prefix that is prepended to all keys to easily scope access to localStorage.
//
//      2. Support storing retrieving typed values
//          Internally, localStorage stores everything as a string.  If you put in an integer or
//          float, for example, retrieving the value from localStorage will always return a string.
//          This class adds typed retrieval methods that will automatically parse the string
//          into the appropriate type.
//
//          This class supports storing and retrieving more complex types (such as arrays and objects)
//          by first serializing the value to JSON.  Remember that each domain is limited to around
//          5 MB of localStorage, so be careful storing large objects/arrays.
//
//          Supported types:  boolean, integer, float, object, array, and date.
//
//      3. Setting a key to undefined or null will remove the key from localStorage.
//
// Usage:
//      To use this class, you must create a new instance of it and provide a prefix for all keys.
//      The prefix must be non-null and not empty string.  Prefixes should be globally unique
//      across all Sharotica code.
//
//      var sharoticaStorage = new LocalStorage("shar");
//
//      // Check if user has liked photo "1234" (assume there is nothing in local storage):
//      var likes1234 = sharoticaStorage.getBoolean("1234");  // returns false since there is nothing in localStorage
//      var notTyped = sharoticaStorage.get("1234");          // returns undefined since there is nothing in localStorage
//
//      // Record that the user has liked photo "1234":
//      sharoticaStorage.set("1234", true);                   // stores the value in localStorage under the key: _shar.likes.1234
//      likes1234 = sharoticaStorage.getBoolean("1234");      // returns true since the value was written into localStorage
//
//      sharoticaStorage.set("myObjName", myObj); // stores the given object serialized as json into localStorage ('angular.toJson(myObj)' shouldn't be needed)
//      sharoticaStorage.get("myObjName");                        // returns the object as a JSON serialized string
//      sharoticaStorage.getObject("myObjName");                  // returns the actual object (i.e. JSON deserialization is performed for you, no need for 'angular.fromJson(sharoticaStorage.get("myObjName"))').
//
sharoticaApp.factory("LocalStorage",
	[       "$window", "$log", "Class",
	function($window,   $log,   Class) {

	// Since we may use localStorage on a client domain, all keys we store in localStorage get
	// scoped with the "_shar." prefix to reduce the chance of collisions.
	var SHAR_PREFIX = "_shar.";

	// Since localStorage stores everything as a String, boolean values would be stored as
	// "true" and "false" by default.  There's really no reason to use up unnecessary space
	// to store the words "true" and "false", so instead this class stores boolean values as
	// "T" and "F".  Since localStorage is limited (and there is no mechanism to increase the
	// available storage), every character counts.
	var TRUE = "T";
	var FALSE = "F";

	// Get reference to browser's localStorage interface.  If not available, then an error is logged
	// and all methods on LocalStorage instances will be no-ops.  All of the browser's that we support
	// have support for localStorage, so this will only be an issue for non-supported browsers.
	// It's important that we do not throw errors on unsupported browsers.  The experience will
	// obviously be degraded in some way, but we do not want to entirely prevent the user from using
	// the app.
	var localStorage = $window && $window['localStorage'];
	if (!localStorage) {
		$log.error("Local Storage is not supported on this browser.");
	}

	// angular.fromJson bound to angular so that it can be passed around as a function.
	var parseJson = angular.bind(angular, angular.fromJson);

	// Generates the fully scoped key name.
	//
	// scopeKey is a private function that is invoked using scopeKey.call(localStorageInstance, key);
	function scopeKey(key) {
		return !key ? null : this.prefix + key;
	}

	/**
	 * Parses the value of the given key using the provided parse function.
	 * If successfully parsed, the parsed value is returned.  If the value is
	 * not set or if the value cannot be parsed, then the defaultValue is returned.
	 */
	// Private function - this is an instance of LocalStorage class.
	function getParsedValue(key, parseFunc, type, defaultValue) {
		var value = this.get(key);
		if (value) {
			try {
				return parseFunc.call(this, value);
			} catch(e) {
				$log.warn("Unable to parse ", value, " as a ", type, "  Returning defalut value: ", defaultValue);
			}
		}

		return defaultValue;
	}

	var LocalStorage = Class.extend({
		init: function(prefix) {
			if (!prefix || !angular.isString(prefix)) {
				throw new Error("Local storage key prefix must be a non-empty string: received prefix=" + prefix);
			}

			this.prefix = SHAR_PREFIX + prefix;
			// Ensure that this.prefix always ends in a "."
			if (prefix.charAt(prefix.length - 1) !== ".") {
				this.prefix += ".";
			}
		},

		/**
		 * Gets an unparsed value from localStorage.  If localStorage is not supported,
		 * then null is returned.
		 */
		get: function(key) {
			var scopedKey = scopeKey.call(this, key);
			if (!scopedKey || !localStorage) {
				return null;
			}

			return localStorage[scopedKey];
		},

		/**
		 * Gets the
		 */
		getBoolean: function(key, defaultValue) {
			var value = this.get(key);
			return (value && value !== FALSE) || (defaultValue || false);
		},

		getInteger: function(key, defaultValue) {
			return getParsedValue.call(this, key, parseInt, "integer", defaultValue);
		},

		getFloat: function(key, defaultValue) {
			return getParsedValue.call(this, key, parseFloat, "float", defaultValue);
		},

		getObject: function(key, defaultValue) {
			return getParsedValue.call(this, key, parseJson, "json", defaultValue);
		},

		getDate: function(key, defaultValue) {
			var value = getParsedValue.call(this, key, parseInt, "integer", -1);
			return value === -1 ? defaultValue : new Date(value);
		},

		set: function(key, value) {
			if (angular.isUndefined(value) || value === null) {
				this.remove(key);
			}

			var fullKey = scopeKey.call(this, key);
			if (!fullKey) {
				return;
			}

			var storeValue = value;
			if (typeof value === "boolean") {
				storeValue = value ? TRUE : FALSE;
			} else if (angular.isArray(value) || angular.isObject(value)) {
				storeValue = angular.toJson(value, false);
			} else if (angular.isDate(value)) {
				// Store dates as number of milliseconds since epoch since that is shorter
				// than storing the date formatted as a string.
				storeValue = +value;
			}

			localStorage[fullKey] = storeValue;
		},

		remove: function(key) {
			var fullKey = scopeKey.call(this, key);
			if (!fullKey) {
				return;
			}

			localStorage.removeItem(fullKey);
		}
	});

	return LocalStorage;

}]);

sharoticaApp.factory("Class", function() {
	// Source: http://ejohn.org/blog/simple-javascript-inheritance/
	/*
	 * Simple JavaScript Inheritance
	 * By John Resig http://ejohn.org/
	 * MIT Licensed.
	 */
	// Inspired by base2 and Prototype
	var initializing = false,
		fnTest = /xyz/.test(function(){xyz;}) ? /\b_super\b/ : /.*/;

	// The base Class implementation (does nothing)
	var Class = function(){};

	// Create a new Class that inherits from this class
	Class.extend = function(prop) {
		var _super = this.prototype;

		// Instantiate a base class (but only create the instance,
		// don't run the init constructor)
		initializing = true;
		var prototype = new this();
		initializing = false;

		// Copy the properties over onto the new prototype
		for (var name in prop) {
			// Check if we're overwriting an existing function
			prototype[name] = typeof prop[name] == "function" &&
				typeof _super[name] == "function" && fnTest.test(prop[name]) ?
				(function(name, fn){
					return function() {
						var tmp = this._super;

						// Add a new ._super() method that is the same method
						// but on the super-class
						this._super = _super[name];
					   
						// The method only need to be bound temporarily, so we
						// remove it when we're done executing
						var ret = fn.apply(this, arguments);        
						this._super = tmp;
					   
						return ret;
					};
				})(name, prop[name]) :
				prop[name];
		}

		// The dummy class constructor
		function Class() {
		  // All construction is actually done in the init method
		  if ( !initializing && this.init )
			this.init.apply(this, arguments);
		}

		// Populate our constructed prototype object
		Class.prototype = prototype;

		// Enforce the constructor to be what we expect
		Class.prototype.constructor = Class;

		// And make this class extendable
		Class.extend = arguments.callee;

		return Class;
	};

	return Class;
});