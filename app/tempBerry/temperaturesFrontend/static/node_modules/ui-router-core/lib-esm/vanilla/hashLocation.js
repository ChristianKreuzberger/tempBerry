/**
 * @internalapi
 * @module vanilla
 */ /** */
import { isDefined } from "../common/index";
import { splitHash, splitQuery, trimHashVal, getParams, locationPluginFactory, buildUrl } from "./utils";
import { pushTo, deregAll } from "../common/common";
import { BrowserLocationConfig } from "./browserLocationConfig";
/** A `LocationServices` that uses the browser hash "#" to get/set the current location */
var HashLocationService = (function () {
    function HashLocationService() {
        var _this = this;
        this._listeners = [];
        this.hash = function () { return splitHash(trimHashVal(location.hash))[1]; };
        this.path = function () { return splitHash(splitQuery(trimHashVal(location.hash))[0])[0]; };
        this.search = function () { return getParams(splitQuery(splitHash(trimHashVal(location.hash))[0])[1]); };
        this.dispose = function () { return deregAll(_this._listeners); };
    }
    HashLocationService.prototype.url = function (url, replace) {
        if (replace === void 0) { replace = true; }
        if (isDefined(url))
            location.hash = url;
        return buildUrl(this);
    };
    HashLocationService.prototype.onChange = function (cb) {
        window.addEventListener('hashchange', cb, false);
        return pushTo(this._listeners, function () { return window.removeEventListener('hashchange', cb); });
    };
    return HashLocationService;
}());
export { HashLocationService };
/** A `UIRouterPlugin` uses the browser hash to get/set the current location */
export var hashLocationPlugin = locationPluginFactory('vanilla.hashBangLocation', false, HashLocationService, BrowserLocationConfig);
//# sourceMappingURL=hashLocation.js.map