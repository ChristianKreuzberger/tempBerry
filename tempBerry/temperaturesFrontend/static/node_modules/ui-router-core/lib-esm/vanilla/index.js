import { services } from "../common/coreservices";
import { $q } from "./$q";
import { $injector } from "./$injector";
export { $q, $injector };
export function servicesPlugin(router) {
    services.$injector = $injector;
    services.$q = $q;
    return { name: "vanilla.services", $q: $q, $injector: $injector, dispose: function () { return null; } };
}
export * from "./hashLocation";
export * from "./memoryLocation";
export * from "./pushStateLocation";
//# sourceMappingURL=index.js.map