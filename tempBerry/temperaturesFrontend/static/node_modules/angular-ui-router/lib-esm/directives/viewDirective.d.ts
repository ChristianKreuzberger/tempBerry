import { ActiveUIView } from "ui-router-core";
import { Ng1ViewConfig } from "../statebuilders/views";
/** @hidden */
export declare type UIViewData = {
    $cfg: Ng1ViewConfig;
    $uiView: ActiveUIView;
};
/** @hidden */
export declare type UIViewAnimData = {
    $animEnter: Promise<any>;
    $animLeave: Promise<any>;
    $$animLeave: {
        resolve: () => any;
    };
};
