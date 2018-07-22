"use strict";
var __assign = (this && this.__assign) || Object.assign || function(t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
        s = arguments[i];
        for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
            t[p] = s[p];
    }
    return t;
};
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * @internalapi
 * @module url
 */ /** for typedoc */
var common_1 = require("../common/common");
var predicates_1 = require("../common/predicates");
var urlMatcher_1 = require("./urlMatcher");
var param_1 = require("../params/param");
var paramTypes_1 = require("../params/paramTypes");
/** @internalapi */
var ParamFactory = /** @class */ (function () {
    function ParamFactory(umf) {
        this.umf = umf;
    }
    ParamFactory.prototype.fromConfig = function (id, type, state) {
        return new param_1.Param(id, type, param_1.DefType.CONFIG, this.umf, state);
    };
    ParamFactory.prototype.fromPath = function (id, type, state) {
        return new param_1.Param(id, type, param_1.DefType.PATH, this.umf, state);
    };
    ParamFactory.prototype.fromSearch = function (id, type, state) {
        return new param_1.Param(id, type, param_1.DefType.SEARCH, this.umf, state);
    };
    return ParamFactory;
}());
exports.ParamFactory = ParamFactory;
/**
 * Factory for [[UrlMatcher]] instances.
 *
 * The factory is available to ng1 services as
 * `$urlMatcherFactory` or ng1 providers as `$urlMatcherFactoryProvider`.
 */
var UrlMatcherFactory = /** @class */ (function () {
    function UrlMatcherFactory() {
        /** @hidden */ this.paramTypes = new paramTypes_1.ParamTypes();
        /** @hidden */ this._isCaseInsensitive = false;
        /** @hidden */ this._isStrictMode = true;
        /** @hidden */ this._defaultSquashPolicy = false;
        /** @internalapi Creates a new [[Param]] for a given location (DefType) */
        this.paramFactory = new ParamFactory(this);
        common_1.extend(this, { UrlMatcher: urlMatcher_1.UrlMatcher, Param: param_1.Param });
    }
    /** @inheritdoc */
    UrlMatcherFactory.prototype.caseInsensitive = function (value) {
        return (this._isCaseInsensitive = predicates_1.isDefined(value) ? value : this._isCaseInsensitive);
    };
    /** @inheritdoc */
    UrlMatcherFactory.prototype.strictMode = function (value) {
        return (this._isStrictMode = predicates_1.isDefined(value) ? value : this._isStrictMode);
    };
    /** @inheritdoc */
    UrlMatcherFactory.prototype.defaultSquashPolicy = function (value) {
        if (predicates_1.isDefined(value) && value !== true && value !== false && !predicates_1.isString(value))
            throw new Error("Invalid squash policy: " + value + ". Valid policies: false, true, arbitrary-string");
        return (this._defaultSquashPolicy = predicates_1.isDefined(value) ? value : this._defaultSquashPolicy);
    };
    /**
     * Creates a [[UrlMatcher]] for the specified pattern.
     *
     * @param pattern  The URL pattern.
     * @param config  The config object hash.
     * @returns The UrlMatcher.
     */
    UrlMatcherFactory.prototype.compile = function (pattern, config) {
        // backward-compatible support for config.params -> config.state.params
        var params = config && !config.state && config.params;
        config = params ? __assign({ state: { params: params } }, config) : config;
        var globalConfig = { strict: this._isStrictMode, caseInsensitive: this._isCaseInsensitive };
        return new urlMatcher_1.UrlMatcher(pattern, this.paramTypes, this.paramFactory, common_1.extend(globalConfig, config));
    };
    /**
     * Returns true if the specified object is a [[UrlMatcher]], or false otherwise.
     *
     * @param object  The object to perform the type check against.
     * @returns `true` if the object matches the `UrlMatcher` interface, by
     *          implementing all the same methods.
     */
    UrlMatcherFactory.prototype.isMatcher = function (object) {
        // TODO: typeof?
        if (!predicates_1.isObject(object))
            return false;
        var result = true;
        common_1.forEach(urlMatcher_1.UrlMatcher.prototype, function (val, name) {
            if (predicates_1.isFunction(val))
                result = result && (predicates_1.isDefined(object[name]) && predicates_1.isFunction(object[name]));
        });
        return result;
    };
    /**
     * Creates and registers a custom [[ParamType]] object
     *
     * A [[ParamType]] can be used to generate URLs with typed parameters.
     *
     * @param name  The type name.
     * @param definition The type definition. See [[ParamTypeDefinition]] for information on the values accepted.
     * @param definitionFn A function that is injected before the app runtime starts.
     *        The result of this function should be a [[ParamTypeDefinition]].
     *        The result is merged into the existing `definition`.
     *        See [[ParamType]] for information on the values accepted.
     *
     * @returns - if a type was registered: the [[UrlMatcherFactory]]
     *   - if only the `name` parameter was specified: the currently registered [[ParamType]] object, or undefined
     *
     * Note: Register custom types *before using them* in a state definition.
     *
     * See [[ParamTypeDefinition]] for examples
     */
    UrlMatcherFactory.prototype.type = function (name, definition, definitionFn) {
        var type = this.paramTypes.type(name, definition, definitionFn);
        return !predicates_1.isDefined(definition) ? type : this;
    };
    /** @hidden */
    UrlMatcherFactory.prototype.$get = function () {
        this.paramTypes.enqueue = false;
        this.paramTypes._flushTypeQueue();
        return this;
    };
    /** @internalapi */
    UrlMatcherFactory.prototype.dispose = function () {
        this.paramTypes.dispose();
    };
    return UrlMatcherFactory;
}());
exports.UrlMatcherFactory = UrlMatcherFactory;
//# sourceMappingURL=urlMatcherFactory.js.map