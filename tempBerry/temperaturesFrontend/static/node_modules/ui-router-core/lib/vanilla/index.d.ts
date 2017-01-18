/**
 * Naive, pure JS implementation of core ui-router services
 *
 *
 * @internalapi
 * @module vanilla
 */ /** */
import { UIRouter } from "../router";
import { ServicesPlugin } from "./interface";
import { $q } from "./$q";
import { $injector } from "./$injector";
export { $q, $injector };
export declare function servicesPlugin(router: UIRouter): ServicesPlugin;
export * from "./hashLocation";
export * from "./memoryLocation";
export * from "./pushStateLocation";
