"use strict";
function __export(m) {
    for (var p in m) if (!exports.hasOwnProperty(p)) exports[p] = m[p];
}
var coreservices_1 = require("../common/coreservices");
var _q_1 = require("./$q");
exports.$q = _q_1.$q;
var _injector_1 = require("./$injector");
exports.$injector = _injector_1.$injector;
function servicesPlugin(router) {
    coreservices_1.services.$injector = _injector_1.$injector;
    coreservices_1.services.$q = _q_1.$q;
    return { name: "vanilla.services", $q: _q_1.$q, $injector: _injector_1.$injector, dispose: function () { return null; } };
}
exports.servicesPlugin = servicesPlugin;
__export(require("./hashLocation"));
__export(require("./memoryLocation"));
__export(require("./pushStateLocation"));
//# sourceMappingURL=index.js.map