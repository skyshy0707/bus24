<template>

    <div style="flex-direction: column;">

        <p>Наши автобусы:</p>
        <Scroll
            :enabledCrud="true"
            :endpoint="'my-buses'"
            :itemView="itemView"
            @delete="delete_"
            @get="view"
        >
        </Scroll>

        <ModelComponent
            :actionType="actionTypeValue"
            :object="objectValue"
            :crudModel="unitApi"
            v-model:objectValue="objectValue"
            v-model:actionTypeValue="actionTypeValue"
        >
        </ModelComponent>

        <p>Автобусы, подходящие для лида:</p>
        <ChangeUnitSet
            v-if="$lead?.lead?.capacity_class"
            v-model:set="set"
            :enabledCrud="true"
            :endpoint="`unit-accepting-lead/${$lead?.lead?.capacity_class}`"
            :button_send_set="'🚌➕'"
            :change_type="'add'"
            :mark_element_action_as="'add'"
            :where_emit="'addUnitsToLead'"
            @addUnitsToLead="addUnitsToLead"
            @delete="delete_"
            @get="view"
        >
        </ChangeUnitSet>

    </div>

</template>

<script lang="ts">
import { defineComponent, type PropType, reactive } from 'vue'

import type { CrudModel } from "@shared/types/interfaces"
import type { Id } from "@shared/types/types"
import { isEqual } from "@shared/lib/format"

import { UnitApi } from "entities/unit/api/unit"
import type { UnitState, UnitView } from 'entities/unit/types'
import type { LeadState } from 'entities/lead/types'


import { changeLeadUnitSet } from "features/attach-detach-unitset-btn/api/change"
import type { ChangeUnitSetParams } from "features/attach-detach-unitset-btn/types"

import { ModelControlPanel } from "widgets/model-control-panel"
import type { SafeBaseComponent } from "widgets/types"

const unitApi = reactive(new UnitApi())


const UnitPanel = defineComponent({

    mixins: [
        ModelControlPanel as any,
    ],

    inject: {
        $lead: {
            from: '$lead',
            default: () => null as { lead: LeadState } | null
        },
        $unit: {
            from: '$unit',
            default: () => null as { unit: UnitState } | null
        }
    },

    data(){
        return {
            unitApi,
            set: [] as Array<Id>,
            itemView: {
                fieldName: 'bort',
                icon: '🚌'
            },
            form: false
        }
    },
    watch: {
        $unit: {
            handler(newValue){
                if (newValue){
                    this.objectValue = newValue.unit
                }
            },
            deep: true,
            immediate: true
        }
    },
    props: {
        object: {
            type: Object as PropType<UnitView>,
            required: false,
            default: () => unitApi.defaultObject
        },
        crudModel: {
            type: Object as PropType<CrudModel>,
            default: () => (new UnitApi()),
            required: false
        },
    }, 
    methods: {
        //...(BaseCrud.methods as Record<string, Function>),
        async addUnitsToLead(data: ChangeUnitSetParams){
            const lead = this.$lead.lead
            console.log(`addUnitsToLead: ${Object.keys(data)}`)
            console.log(`addUnitsToLead data.units: ${data.units}`)

            const response = await changeLeadUnitSet(lead.id, data)

            if (response.status == 200){
                this.set = []
            }
        }
    }
})

export default UnitPanel as typeof UnitPanel & SafeBaseComponent
</script>