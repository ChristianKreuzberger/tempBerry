/**
 * @coreapi
 * @module core
 */ /** */
import { StateParams } from "./params/stateParams";
import { Queue } from "./common/queue";
import { copy } from "./common/common";
/**
 * Global mutable state
 */
var Globals = (function () {
    function Globals(transitionService) {
        var _this = this;
        this.params = new StateParams();
        this.transitionHistory = new Queue([], 1);
        this.successfulTransitions = new Queue([], 1);
        var beforeNewTransition = function ($transition$) {
            _this.transition = $transition$;
            _this.transitionHistory.enqueue($transition$);
            var updateGlobalState = function () {
                _this.successfulTransitions.enqueue($transition$);
                _this.$current = $transition$.$to();
                _this.current = _this.$current.self;
                copy($transition$.params(), _this.params);
            };
            $transition$.onSuccess({}, updateGlobalState, { priority: 10000 });
            var clearCurrentTransition = function () { if (_this.transition === $transition$)
                _this.transition = null; };
            $transition$.promise.then(clearCurrentTransition, clearCurrentTransition);
        };
        transitionService.onBefore({}, beforeNewTransition);
    }
    return Globals;
}());
export { Globals };
//# sourceMappingURL=globals.js.map