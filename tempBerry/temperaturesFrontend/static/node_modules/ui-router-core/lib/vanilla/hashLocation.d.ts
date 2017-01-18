import { LocationServices } from "../common/coreservices";
import { UIRouter } from "../router";
import { LocationPlugin } from "./interface";
import { Disposable } from "../interface";
/** A `LocationServices` that uses the browser hash "#" to get/set the current location */
export declare class HashLocationService implements LocationServices, Disposable {
    private _listeners;
    hash: () => string;
    path: () => string;
    search: () => any;
    url(url?: string, replace?: boolean): string;
    onChange(cb: EventListener): Function;
    dispose: () => void;
}
/** A `UIRouterPlugin` uses the browser hash to get/set the current location */
export declare const hashLocationPlugin: (router: UIRouter) => LocationPlugin;
