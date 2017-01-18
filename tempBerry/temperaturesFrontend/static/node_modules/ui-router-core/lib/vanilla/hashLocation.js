"use strict";
/**
 * @internalapi
 * @module vanilla
 */ /** */
var index_1 = require("../common/index");
var utils_1 = require("./utils");
var common_1 = require("../common/common");
var browserLocationConfig_1 = require("./browserLocationConfig");
/** A `LocationServices` that uses the browser hash "#" to get/set the current location */
var HashLocationService = (function () {
    function HashLocationService() {
        var _this = this;
        this._listeners = [];
        this.hash = function () { return utils_1.splitHash(utils_1.trimHashVal(location.hash))[1]; };
        this.path = function () { return utils_1.splitHash(utils_1.splitQuery(utils_1.trimHashVal(location.hash))[0])[0]; };
        this.search = function () { return utils_1.getParams(utils_1.splitQuery(utils_1.splitHash(utils_1.trimHashVal(location.hash))[0])[1]); };
        this.dispose = function () { return common_1.deregAll(_this._listeners); };
    }
    HashLocationService.prototype.url = function (url, replace) {
        if (replace === void 0) { replace = true; }
        if (index_1.isDefined(url))
            location.hash = url;
        return utils_1.buildUrl(this);
    };
    HashLocationService.prototype.onChange = function (cb) {
        window.addEventListener('hashchange', cb, false);
        return common_1.pushTo(this._listeners, function () { return window.removeEventListener('hashchange', cb); });
    };
    return HashLocationService;
}());
exports.HashLocationService = HashLocationService;
/** A `UIRouterPlugin` uses the browser hash to get/set the current location */
exports.hashLocationPlugin = utils_1.locationPluginFactory('vanilla.hashBangLocation', false, HashLocationService, browserLocationConfig_1.BrowserLocationConfig);
//# sourceMappingURL=hashLocation.js.map