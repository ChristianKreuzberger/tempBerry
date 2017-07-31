/**
 * @coreapi
 * @module core
 */ /** */
import { UrlMatcherFactory } from "./url/urlMatcherFactory";
import { UrlRouter } from "./url/urlRouter";
import { TransitionService } from "./transition/transitionService";
import { ViewService } from "./view/view";
import { StateRegistry } from "./state/stateRegistry";
import { StateService } from "./state/stateService";
import { UIRouterGlobals } from "./globals";
import { UIRouterPlugin, Disposable } from "./interface";
import { UrlService } from "./url/urlService";
import { LocationServices, LocationConfig } from "./common/coreservices";
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
export declare class UIRouter {
    locationService: LocationServices;
    locationConfig: LocationConfig;
    /** @hidden */
    $id: number;
    viewService: ViewService;
    transitionService: TransitionService;
    globals: UIRouterGlobals;
    urlMatcherFactory: UrlMatcherFactory;
    urlRouter: UrlRouter;
    stateRegistry: StateRegistry;
    stateService: StateService;
    urlService: UrlService;
    private _disposables;
    /** Registers an object to be notified when the router is disposed */
    disposable(disposable: Disposable): void;
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
    dispose(disposable?: any): void;
    constructor(locationService?: LocationServices, locationConfig?: LocationConfig);
    /** @hidden */
    private _plugins;
    /**
     * Adds a plugin to UI-Router
     *
     * This method adds a UI-Router Plugin.
     * A plugin can enhance or change UI-Router behavior using any public API.
     *
     * #### Example:
     * ```js
     * import { MyCoolPlugin } from "ui-router-cool-plugin";
     *
     * var plugin = router.addPlugin(MyCoolPlugin);
     * ```
     *
     * ### Plugin authoring
     *
     * A plugin is simply a class (or constructor function) which accepts a [[UIRouter]] instance and (optionally) an options object.
     *
     * The plugin can implement its functionality using any of the public APIs of [[UIRouter]].
     * For example, it may configure router options or add a Transition Hook.
     *
     * The plugin can then be published as a separate module.
     *
     * #### Example:
     * ```js
     * export class MyAuthPlugin implements UIRouterPlugin {
     *   constructor(router: UIRouter, options: any) {
     *     this.name = "MyAuthPlugin";
     *     let $transitions = router.transitionService;
     *     let $state = router.stateService;
     *
     *     let authCriteria = {
     *       to: (state) => state.data && state.data.requiresAuth
     *     };
     *
     *     function authHook(transition: Transition) {
     *       let authService = transition.injector().get('AuthService');
     *       if (!authService.isAuthenticated()) {
     *         return $state.target('login');
     *       }
     *     }
     *
     *     $transitions.onStart(authCriteria, authHook);
     *   }
     * }
     * ```
     *
     * @param plugin one of:
     *        - a plugin class which implements [[UIRouterPlugin]]
     *        - a constructor function for a [[UIRouterPlugin]] which accepts a [[UIRouter]] instance
     *        - a factory function which accepts a [[UIRouter]] instance and returns a [[UIRouterPlugin]] instance
     * @param options options to pass to the plugin class/factory
     * @returns the registered plugin instance
     */
    plugin<T extends UIRouterPlugin>(plugin: {
        new (router: UIRouter, options?: any): T;
    }, options?: any): T;
    /** Allow javascript constructor function */
    plugin<T extends UIRouterPlugin>(plugin: {
        (router: UIRouter, options?: any): void;
    }, options?: any): T;
    /** Allow javascript factory function */
    plugin<T extends UIRouterPlugin>(plugin: PluginFactory<T>, options?: any): T;
    /**
     * Returns registered plugins
     *
     * Returns the registered plugin of the given `pluginName`.
     * If no `pluginName` is given, returns all registered plugins
     *
     * @param pluginName (optional) the name of the plugin to get
     * @return the named plugin (undefined if not found), or all plugins (if `pluginName` is omitted)
     */
    getPlugin(): UIRouterPlugin[];
    getPlugin(pluginName?: string): UIRouterPlugin;
}
export declare type PluginFactory<T> = (router: UIRouter, options?: any) => T;
