import type { Component, ExtractPropTypes } from 'vue'
import { type AsyncComponentLoader, defineAsyncComponent } from "vue"

import { settings } from "entities/model_component/lib/component/settings"

//for implementin example:
import type { PropType } from 'vue'
import { Lead } from "entities/lead"
import { LeadApi } from "entities/lead/api/lead"
import type { LeadView } from "entities/lead/types"


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

const example = {
    object: Object as PropType<LeadView>,
    api: LeadApi
}


//generateModelComponent(Lead, example)

export {
    generateModelComponent, getComponentByModel
}