"use strict";
/**
 * @coreapi
 * @module core
 */ /** */
var urlMatcherFactory_1 = require("./url/urlMatcherFactory");
var urlRouter_1 = require("./url/urlRouter");
var transitionService_1 = require("./transition/transitionService");
var view_1 = require("./view/view");
var stateRegistry_1 = require("./state/stateRegistry");
var stateService_1 = require("./state/stateService");
var globals_1 = require("./globals");
var common_1 = require("./common/common");
var predicates_1 = require("./common/predicates");
var urlService_1 = require("./url/urlService");
/** @hidden */
var _routerInstance = 0;
/**
 * The master class used to instantiate an instance of UI-Router.
 *
 * UI-Router (for a specific framework) will create an instance of this class during bootstrap.
 * This class instantiates and wires the UI-Router services together.
 *
 * After a new instance of the UIRouter class is created, it should be configured for your app.
 * For instance, app states should be registered with the [[stateRegistry]].
 *
 * Tell UI-Router to monitor the URL by calling `uiRouter.urlRouter.listen()` ([[UrlRouter.listen]])
 */
var UIRouter = (function () {
    function UIRouter(locationService, locationConfig) {
        if (locationService === void 0) { locationService = urlService_1.UrlService.locationServiceStub; }
        if (locationConfig === void 0) { locationConfig = urlService_1.UrlService.locationConfigStub; }
        this.locationService = locationService;
        this.locationConfig = locationConfig;
        /** @hidden */
        this.$id = _routerInstance++;
        this.viewService = new view_1.ViewService();
        this.transitionService = new transitionService_1.TransitionService(this);
        this.globals = new globals_1.Globals(this.transitionService);
        this.urlMatcherFactory = new urlMatcherFactory_1.UrlMatcherFactory();
        this.urlRouter = new urlRouter_1.UrlRouter(this);
        this.stateRegistry = new stateRegistry_1.StateRegistry(this);
        this.stateService = new stateService_1.StateService(this);
        this.urlService = new urlService_1.UrlService(this);
        this._disposables = [];
        /** @hidden */
        this._plugins = {};
        this.viewService._pluginapi._rootViewContext(this.stateRegistry.root());
        this.globals.$current = this.stateRegistry.root();
        this.globals.current = this.globals.$current.self;
        this.disposable(this.transitionService);
        this.disposable(this.urlRouter);
        this.disposable(this.stateRegistry);
        this.disposable(locationService);
        this.disposable(locationConfig);
    }
    /** Registers an object to be notified when the router is disposed */
    UIRouter.prototype.disposable = function (disposable) {
        this._disposables.push(disposable);
    };
    /**
     * Disposes this router instance
     *
     * When called, clears resources retained by the router by calling `dispose(this)` on all
     * registered [[disposable]] objects.
     *
     * Or, if a `disposable` object is provided, calls `dispose(this)` on that object only.
     *
     * @param disposable (optional) the disposable to dispose
     */
    UIRouter.prototype.dispose = function (disposable) {
        var _this = this;
        if (disposable && predicates_1.isFunction(disposable.dispose)) {
            disposable.dispose(this);
            return undefined;
        }
        this._disposables.slice().forEach(function (d) {
            try {
                typeof d.dispose === 'function' && d.dispose(_this);
                common_1.removeFrom(_this._disposables, d);
            }
            catch (ignored) { }
        });
    };
    /** Allow javascript factory function */
    UIRouter.prototype.plugin = function (plugin, options) {
        if (options === void 0) { options = {}; }
        var pluginInstance = new plugin(this, options);
        if (!pluginInstance.name)
            throw new Error("Required property `name` missing on plugin: " + pluginInstance);
        this._disposables.push(pluginInstance);
        return this._plugins[pluginInstance.name] = pluginInstance;
    };
    UIRouter.prototype.getPlugin = function (pluginName) {
        return pluginName ? this._plugins[pluginName] : common_1.values(this._plugins);
    };
    return UIRouter;
}());
exports.UIRouter = UIRouter;
//# sourceMappingURL=router.js.map