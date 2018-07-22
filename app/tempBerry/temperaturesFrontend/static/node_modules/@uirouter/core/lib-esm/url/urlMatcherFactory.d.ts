import { UrlMatcher } from './urlMatcher';
import { Param } from '../params/param';
import { ParamTypes } from '../params/paramTypes';
import { ParamTypeDefinition } from '../params/interface';
import { Disposable } from '../interface';
import { ParamType } from '../params/paramType';
import { UrlMatcherCompileConfig, UrlMatcherConfig } from './interface';
import { StateDeclaration } from '../state';
/** @internalapi */
export declare class ParamFactory {
    private umf;
    fromConfig(id: string, type: ParamType, state: StateDeclaration): Param;
    fromPath(id: string, type: ParamType, state: StateDeclaration): Param;
    fromSearch(id: string, type: ParamType, state: StateDeclaration): Param;
    constructor(umf: UrlMatcherFactory);
}
/**
 * Factory for [[UrlMatcher]] instances.
 *
 * The factory is available to ng1 services as
 * `$urlMatcherFactory` or ng1 providers as `$urlMatcherFactoryProvider`.
 */
export declare class UrlMatcherFactory implements Disposable, UrlMatcherConfig {
    /** @hidden */ paramTypes: ParamTypes;
    /** @hidden */ _isCaseInsensitive: boolean;
    /** @hidden */ _isStrictMode: boolean;
    /** @hidden */ _defaultSquashPolicy: boolean | string;
    /** @internalapi Creates a new [[Param]] for a given location (DefType) */
    paramFactory: ParamFactory;
    constructor();
    /** @inheritdoc */
    caseInsensitive(value?: boolean): boolean;
    /** @inheritdoc */
    strictMode(value?: boolean): boolean;
    /** @inheritdoc */
    defaultSquashPolicy(value?: boolean | string): string | boolean;
    /**
     * Creates a [[UrlMatcher]] for the specified pattern.
     *
     * @param pattern  The URL pattern.
     * @param config  The config object hash.
     * @returns The UrlMatcher.
     */
    compile(pattern: string, config?: UrlMatcherCompileConfig): UrlMatcher;
    /**
     * Returns true if the specified object is a [[UrlMatcher]], or false otherwise.
     *
     * @param object  The object to perform the type check against.
     * @returns `true` if the object matches the `UrlMatcher` interface, by
     *          implementing all the same methods.
     */
    isMatcher(object: any): boolean;
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
    type(name: string, definition?: ParamTypeDefinition, definitionFn?: () => ParamTypeDefinition): any;
    /** @hidden */
    $get(): this;
    /** @internalapi */
    dispose(): void;
}
