import { type PropType } from 'vue'

import { Crud } from "@shared/model/crud"
import type { CrudModel } from "@shared/types/interfaces"
import type { Id, Response } from '@shared/types/types'
import * as validators from "@shared/types/validators"
import { Scroll } from "@shared/ui"

import { ModelComponent } from "entities/model_component"

import { ChangeUnitSet } from "widgets/attach-detach-unitset"

export const ModelControlPanel = {
    components: {
        ChangeUnitSet,
        ModelComponent, 
        Scroll
    },
    computed: {
        api() { 
            return new Crud(this.crudModel) 
        }
    },
    data(){
        return {
            actionTypeValue: this.actionType,
            objectValue: this.object,
        }
    },
    props: {
        actionType: {
            type: String as PropType<string>,
            validator: validators.actionType,
            default: () => 'create'
        },
        crudModel: {
            type: Object as PropType<CrudModel>,
            required: true
        },
        object: {
            type: Object as PropType<Object>,
            required: true
        }
    },
    methods: {
        async view(id: Id): Promise<Response> {
            const response = await this.api.get(id)
            if (response.status == 200 || response.response_status == 200){
                this.objectValue = response.data
                this.actionTypeValue = 'view'
            }
            return response
        },
        async delete_(id: Id): Promise<Id>{
            await this.api.delete(id)
            return id
        },
    }
}