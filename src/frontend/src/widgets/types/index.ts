import { ModelControlPanel } from "widgets/model-control-panel"

type IgnoredPropsForModelComponent = 'crudModel' | 'object'

type SafeBaseComponent = Omit<typeof ModelControlPanel, 'props'> & {
        props: Omit<typeof ModelControlPanel['props'], IgnoredPropsForModelComponent>
    }

export type {
    IgnoredPropsForModelComponent, 
    SafeBaseComponent
}