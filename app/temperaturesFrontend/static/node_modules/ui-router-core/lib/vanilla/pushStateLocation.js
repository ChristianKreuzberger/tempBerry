"use strict";
/**
 * @internalapi
 * @module vanilla
 */ /** */
var index_1 = require("../common/index");
var utils_1 = require("./utils");
var common_1 = require("../common/common");
var browserLocationConfig_1 = require("./browserLocationConfig");
/**
 * A `LocationServices` that gets/sets the current location using the browser's `location` and `history` apis
 *
 * Uses `history.pushState` and `history.replaceState`
 */
var PushStateLocationService = (function () {
    function PushStateLocationService(router) {
        this._listeners = [];
        this._location = location;
        this._history = history;
        this._config = router.urlService.config;
    }
    ;
    PushStateLocationService.prototype.hash = function () {
        return utils_1.trimHashVal(this._location.hash);
    };
    PushStateLocationService.prototype.path = function () {
        var base = this._config.baseHref();
        var path = this._location.pathname;
        var idx = path.indexOf(base);
        if (idx !== 0)
            throw new Error("current url: " + path + " does not start with <base> tag " + base);
        return path.substr(base.length);
    };
    PushStateLocationService.prototype.search = function () {
        return utils_1.getParams(utils_1.splitQuery(this._location.search)[1]);
    };
    PushStateLocationService.prototype.url = function (url, replace, state) {
        if (replace === void 0) { replace = false; }
        if (index_1.isDefined(url)) {
            var fullUrl = this._config.baseHref() + url;
            if (replace)
                this._history.replaceState(state, null, fullUrl);
            else
                this._history.pushState(state, null, fullUrl);
        }
        return utils_1.buildUrl(this);
    };
    PushStateLocationService.prototype.onChange = function (cb) {
        window.addEventListener("popstate", cb, false);
        return common_1.pushTo(this._listeners, function () { return window.removeEventListener("popstate", cb); });
    };
    PushStateLocationService.prototype.dispose = function (router) {
        common_1.deregAll(this._listeners);
    };
    return PushStateLocationService;
}());
exports.PushStateLocationService = PushStateLocationService;
/** A `UIRouterPlugin` that gets/sets the current location using the browser's `location` and `history` apis */
exports.pushStateLocationPlugin = utils_1.locationPluginFactory("vanilla.pushStateLocation", true, PushStateLocationService, browserLocationConfig_1.BrowserLocationConfig);
//# sourceMappingURL=pushStateLocation.js.map