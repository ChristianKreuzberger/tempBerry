/**
 * Main entry point for angular 1.x build
 * @module ng1
 */ /** */
"use strict";
function __export(m) {
    for (var p in m) if (!exports.hasOwnProperty(p)) exports[p] = m[p];
}
var core = require("ui-router-core");
exports.core = core;
__export(require("ui-router-core"));
__export(require("./services"));
__export(require("./statebuilders/views"));
__export(require("./stateProvider"));
require("./injectables");
require("./directives/stateDirectives");
require("./stateFilters");
require("./directives/viewDirective");
require("./viewScroll");
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = "ui.router";
//# sourceMappingURL=index.js.map