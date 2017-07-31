/**
 * @internalapi
 * @module vanilla
 */ /** */
import { isDefined } from "../common/index";
import { splitQuery, getParams, splitHash, locationPluginFactory, buildUrl } from "./utils";
import { removeFrom, deregAll, noop } from "../common/common";
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
        this.hashPrefix = function (newval) { return isDefined(newval) ? _this._hashPrefix = newval : _this._hashPrefix; };
        this.dispose = noop;
    }
    return MemoryLocationConfig;
}());
export { MemoryLocationConfig };
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
        this.dispose = function () { return deregAll(_this._listeners); };
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
        if (isDefined(url)) {
            var path = splitHash(splitQuery(url)[0])[0];
            var hash = splitHash(url)[1];
            var search = getParams(splitQuery(splitHash(url)[0])[1]);
            var oldval = this.url();
            this._url = { path: path, search: search, hash: hash };
            var newval = this.url();
            this._urlChanged(newval, oldval);
        }
        return buildUrl(this);
    };
    MemoryLocationService.prototype.onChange = function (cb) {
        var _this = this;
        this._listeners.push(cb);
        return function () { return removeFrom(_this._listeners, cb); };
    };
    return MemoryLocationService;
}());
export { MemoryLocationService };
/** A `UIRouterPlugin` that gets/sets the current location from an in-memory object */
export var memoryLocationPlugin = locationPluginFactory("vanilla.memoryLocation", false, MemoryLocationService, MemoryLocationConfig);
//# sourceMappingURL=memoryLocation.js.map