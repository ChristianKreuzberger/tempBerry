/**
 * @internalapi
 * @module vanilla
 */ /** */
import { isDefined } from "../common/index";
import { splitQuery, trimHashVal, getParams, locationPluginFactory, buildUrl } from "./utils";
import { pushTo, deregAll } from "../common/common";
import { BrowserLocationConfig } from "./browserLocationConfig";
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
        return trimHashVal(this._location.hash);
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
        return getParams(splitQuery(this._location.search)[1]);
    };
    PushStateLocationService.prototype.url = function (url, replace, state) {
        if (replace === void 0) { replace = false; }
        if (isDefined(url)) {
            var fullUrl = this._config.baseHref() + url;
            if (replace)
                this._history.replaceState(state, null, fullUrl);
            else
                this._history.pushState(state, null, fullUrl);
        }
        return buildUrl(this);
    };
    PushStateLocationService.prototype.onChange = function (cb) {
        window.addEventListener("popstate", cb, false);
        return pushTo(this._listeners, function () { return window.removeEventListener("popstate", cb); });
    };
    PushStateLocationService.prototype.dispose = function (router) {
        deregAll(this._listeners);
    };
    return PushStateLocationService;
}());
export { PushStateLocationService };
/** A `UIRouterPlugin` that gets/sets the current location using the browser's `location` and `history` apis */
export var pushStateLocationPlugin = locationPluginFactory("vanilla.pushStateLocation", true, PushStateLocationService, BrowserLocationConfig);
//# sourceMappingURL=pushStateLocation.js.map