"use strict";
/**
 * @internalapi
 * @module vanilla
 */ /** */
var index_1 = require("../common/index");
var utils_1 = require("./utils");
var common_1 = require("../common/common");
/** A `LocationConfig` mock that gets/sets all config from an in-memory object */
var MemoryLocationConfig = (function () {
    function MemoryLocationConfig() {
        var _this = this;
        this._baseHref = '';
        this._port = 80;
        this._protocol = "http";
        this._host = "localhost";
        this._hashPrefix = "";
        this.port = function () { return _this._port; };
        this.protocol = function () { return _this._protocol; };
        this.host = function () { return _this._host; };
        this.baseHref = function () { return _this._baseHref; };
        this.html5Mode = function () { return false; };
        this.hashPrefix = function (newval) { return index_1.isDefined(newval) ? _this._hashPrefix = newval : _this._hashPrefix; };
        this.dispose = common_1.noop;
    }
    return MemoryLocationConfig;
}());
exports.MemoryLocationConfig = MemoryLocationConfig;
/** A `LocationServices` that gets/sets the current location from an in-memory object */
var MemoryLocationService = (function () {
    function MemoryLocationService() {
        var _this = this;
        this._listeners = [];
        this._url = {
            path: '',
            search: {},
            hash: ''
        };
        this.hash = function () { return _this._url.hash; };
        this.path = function () { return _this._url.path; };
        this.search = function () { return _this._url.search; };
        this.dispose = function () { return common_1.deregAll(_this._listeners); };
    }
    MemoryLocationService.prototype._urlChanged = function (newval, oldval) {
        if (newval === oldval)
            return;
        var evt = new Event("locationchange");
        evt['url'] = newval;
        this._listeners.forEach(function (cb) { return cb(evt); });
    };
    MemoryLocationService.prototype.url = function (url, replace, state) {
        if (replace === void 0) { replace = false; }
        if (index_1.isDefined(url)) {
            var path = utils_1.splitHash(utils_1.splitQuery(url)[0])[0];
            var hash = utils_1.splitHash(url)[1];
            var search = utils_1.getParams(utils_1.splitQuery(utils_1.splitHash(url)[0])[1]);
            var oldval = this.url();
            this._url = { path: path, search: search, hash: hash };
            var newval = this.url();
            this._urlChanged(newval, oldval);
        }
        return utils_1.buildUrl(this);
    };
    MemoryLocationService.prototype.onChange = function (cb) {
        var _this = this;
        this._listeners.push(cb);
        return function () { return common_1.removeFrom(_this._listeners, cb); };
    };
    return MemoryLocationService;
}());
exports.MemoryLocationService = MemoryLocationService;
/** A `UIRouterPlugin` that gets/sets the current location from an in-memory object */
exports.memoryLocationPlugin = utils_1.locationPluginFactory("vanilla.memoryLocation", false, MemoryLocationService, MemoryLocationConfig);
//# sourceMappingURL=memoryLocation.js.map