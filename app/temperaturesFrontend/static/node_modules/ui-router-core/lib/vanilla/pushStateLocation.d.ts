import { LocationServices } from "../common/coreservices";
import { LocationPlugin } from "./interface";
import { UIRouter } from "../router";
import { Disposable } from "../interface";
/**
 * A `LocationServices` that gets/sets the current location using the browser's `location` and `history` apis
 *
 * Uses `history.pushState` and `history.replaceState`
 */
export declare class PushStateLocationService implements LocationServices, Disposable {
    private _listeners;
    private _location;
    private _history;
    private _config;
    constructor(router: UIRouter);
    hash(): string;
    path(): string;
    search(): any;
    url(url?: string, replace?: boolean, state?: any): any;
    onChange(cb: EventListener): Function;
    dispose(router: UIRouter): void;
}
/** A `UIRouterPlugin` that gets/sets the current location using the browser's `location` and `history` apis */
export declare const pushStateLocationPlugin: (router: UIRouter) => LocationPlugin;
