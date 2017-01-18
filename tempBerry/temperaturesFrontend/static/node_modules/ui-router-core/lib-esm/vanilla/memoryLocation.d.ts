import { LocationConfig, LocationServices } from "../common/coreservices";
import { UIRouter } from "../router";
import { LocationPlugin } from "./interface";
import { Disposable } from "../interface";
/** A `LocationConfig` mock that gets/sets all config from an in-memory object */
export declare class MemoryLocationConfig implements LocationConfig {
    _baseHref: string;
    _port: number;
    _protocol: string;
    _host: string;
    _hashPrefix: string;
    port: () => number;
    protocol: () => string;
    host: () => string;
    baseHref: () => string;
    html5Mode: () => boolean;
    hashPrefix: (newval?: any) => any;
    dispose: () => any;
}
/** A `LocationServices` that gets/sets the current location from an in-memory object */
export declare class MemoryLocationService implements LocationServices, Disposable {
    _listeners: Function[];
    _url: {
        path: string;
        search: {};
        hash: string;
    };
    private _urlChanged(newval, oldval);
    hash: () => string;
    path: () => string;
    search: () => {};
    url(url?: string, replace?: boolean, state?: any): string;
    onChange(cb: EventListener): () => Function[];
    dispose: () => void;
}
/** A `UIRouterPlugin` that gets/sets the current location from an in-memory object */
export declare const memoryLocationPlugin: (router: UIRouter) => LocationPlugin;
