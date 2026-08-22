import type { AsyncComponentLoader, Component, ExtractPropTypes } from 'vue'
import { defineAsyncComponent } from 'vue'

import { settings } from "entities/model_component/lib/component/settings"

const componentCache: Record<string, any> = settings.reduce((acc, item) => {
    acc[item.model] = defineAsyncComponent(item.loader as AsyncComponentLoader)
    return acc
}, {} as Record<string, any>)

function generateModelComponent(component: Component, props: Object){
    type BaseProps = ExtractPropTypes<typeof component>
    type GenericComponent = Omit<BaseProps, 'object'> & typeof props

    return component as Component<GenericComponent>
}

function getComponentByModel(model: string){
    return componentCache[model] || 'div'
}

export {
    generateModelComponent, getComponentByModel
}