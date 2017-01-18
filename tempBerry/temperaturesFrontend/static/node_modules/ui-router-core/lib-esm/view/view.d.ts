import { PathNode } from "../path/node";
import { ActiveUIView, ViewContext, ViewConfig } from "./interface";
import { _ViewDeclaration } from "../state/interface";
export declare type ViewConfigFactory = (path: PathNode[], decl: _ViewDeclaration) => ViewConfig | ViewConfig[];
export interface ViewServicePluginAPI {
    _rootViewContext(context?: ViewContext): ViewContext;
    _viewConfigFactory(viewType: string, factory: ViewConfigFactory): any;
    _registeredUIViews(): ActiveUIView[];
    _activeViewConfigs(): ViewConfig[];
}
/**
 * The View service
 *
 * This service pairs existing `ui-view` components (which live in the DOM)
 * with view configs (from the state declaration objects: [[StateDeclaration.views]]).
 *
 * - After a successful Transition, the views from the newly entered states are activated via [[activateViewConfig]].
 *   The views from exited states are deactivated via [[deactivateViewConfig]].
 *   (See: the [[registerActivateViews]] Transition Hook)
 *
 * - As `ui-view` components pop in and out of existence, they register themselves using [[registerUIView]].
 *
 * - When the [[sync]] function is called, the registered `ui-view`(s) ([[UIViewConfig]]
 * are configured with the matching `ViewConfig`(s)  ([[ActiveUIView]]).
 *
 */
export declare class ViewService {
    private _uiViews;
    private _viewConfigs;
    private _rootContext;
    private _viewConfigFactories;
    constructor();
    _pluginapi: ViewServicePluginAPI;
    private _rootViewContext(context?);
    private _viewConfigFactory(viewType, factory);
    createViewConfig(path: PathNode[], decl: _ViewDeclaration): ViewConfig[];
    /**
     * Deactivates a ViewConfig.
     *
     * This function deactivates a `ViewConfig`.
     * After calling [[sync]], it will un-pair from any `ui-view` with which it is currently paired.
     *
     * @param viewConfig The ViewConfig view to deregister.
     */
    deactivateViewConfig(viewConfig: ViewConfig): void;
    activateViewConfig(viewConfig: ViewConfig): void;
    sync(): void;
    /**
     * Registers a `ui-view` component
     *
     * When a `ui-view` component is created, it uses this method to register itself.
     * After registration the [[sync]] method is used to ensure all `ui-view` are configured with the proper [[ViewConfig]].
     *
     * Note: the `ui-view` component uses the `ViewConfig` to determine what view should be loaded inside the `ui-view`,
     * and what the view's state context is.
     *
     * Note: There is no corresponding `deregisterUIView`.
     *       A `ui-view` should hang on to the return value of `registerUIView` and invoke it to deregister itself.
     *
     * @param uiView The metadata for a UIView
     * @return a de-registration function used when the view is destroyed.
     */
    registerUIView(uiView: ActiveUIView): () => void;
    /**
     * Returns the list of views currently available on the page, by fully-qualified name.
     *
     * @return {Array} Returns an array of fully-qualified view names.
     */
    available(): any[];
    /**
     * Returns the list of views on the page containing loaded content.
     *
     * @return {Array} Returns an array of fully-qualified view names.
     */
    active(): any[];
    /**
     * Normalizes a view's name from a state.views configuration block.
     *
     * @param context the context object (state declaration) that the view belongs to
     * @param rawViewName the name of the view, as declared in the [[StateDeclaration.views]]
     *
     * @returns the normalized uiViewName and uiViewContextAnchor that the view targets
     */
    static normalizeUIViewTarget(context: ViewContext, rawViewName?: string): {
        uiViewName: string;
        uiViewContextAnchor: string;
    };
}
