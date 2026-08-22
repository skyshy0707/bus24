<template>

    <ModelComponent
        :actionType="actionTypeValue"
        :object="objectValue"
        :crudModel="leadApi"
        v-model="objectValue"
    >
        <div>
            <p class="model-field">Автобусы на линии:</p>
            <ChangeUnitSet
                v-if="leadProvided"
                :model="'unit'"
                :enabledCrud="true"
                :endpoint="`lead/${objectValue.id}/unit-set`"
                :change_type="'remove'"
                :button_send_set="'➖🚍'"
                :where_emit="'removeBusesFromLead'"
                :itemView="unitItemView"
                @removeBusesFromLead="removeBusesFromLead"
                @deleteUnit="deleteBusUnit"
                @getUnit="getBusUnit"
            >
            </ChangeUnitSet>
        </div>
    </ModelComponent>

    <div>
        <p>Мои созданные заявки:</p>
        <Scroll
            :enabledCrud="true"
            :endpoint="'my-created-leads'"
            :itemView="itemView"
            @delete="delete_"
            @get="view"
        >
        </Scroll>
        <p>Мои принятые заявки:</p>
        <Scroll
            :enabledCrud="true"
            :endpoint="'my-accepted-leads'"
            :itemView="itemView"
            @delete="delete_"
            @get="view"
        >
        </Scroll>
    </div>

</template>

<script lang="ts">
    import { defineComponent, type PropType, reactive } from 'vue'

    import type { CrudModel } from "@shared/types/interfaces"
    import type { Id } from "@shared/types/types"
    
    
    import { LeadApi } from 'entities/lead/api/lead'
    import type { LeadState, LeadView } from 'entities/lead/types';
    import { ProfileStore } from 'entities/profile/ui/Profile'
    import { UnitApi } from 'entities/unit/api/unit'

    import { changeLeadUnitSet } from "features/attach-detach-unitset-btn/api/change"
    import type { ChangeUnitSetParams } from "features/attach-detach-unitset-btn/types"

    import { ModelControlPanel } from "widgets/model-control-panel"
    import type { SafeBaseComponent } from "widgets/types"
    

    const unitApi = reactive(new UnitApi())
    const leadApi = reactive(new LeadApi())

    declare module '@vue/runtime-core' {
        interface ComponentCustomProperties {
            objectValue: LeadView
        }
    }
    const LeadPanel = defineComponent({
        inject: {
            $lead: {
                from: '$lead',
                default: () => null as { lead: LeadState } | null
            }
        },
        mixins: [
            ModelControlPanel as any,
            ProfileStore as any
        ],

        data(){
            return {
                leadApi,
                unitItemView: {
                    fieldName: 'bort',
                    icon: '🚍'
                },
                itemView: {
                    fieldName: 'route_wiki_url',
                    icon: '📰'
                }
            }
        },
        computed: {
            leadProvided(){
                if (this.objectValue.id > 0){
                    return true
                }
                return false
            }
        },
        props: {
            object: {
                type: Object as PropType<LeadView>,
                default: () => (leadApi.defaultObject as unknown as LeadView),
                required: false
            },
            crudModel: {
                type: Object as PropType<CrudModel>,
                default: () => (new LeadApi()),
                required: false
            },
        },
        methods: {
            async removeBusesFromLead(data: ChangeUnitSetParams){
                await changeLeadUnitSet(this.objectValue.id, data)
            },
            async view(id: Id){
                const response = await ModelControlPanel.methods?.view?.call(this, id)
                if (response.status == 200){
                    this.lead.SET_LEAD(response.data as LeadView)
                    this.objectValue = response.data as LeadView
                }
            },
            async deleteBusUnit(id: Id){
                const response = await unitApi.delete(id)
                return response.status == 400 ? null : id
            }, 
            async getBusUnit(id: Id){
                const response = await unitApi.get(id)
                const object = response.data

                if (object) { 
                    this.unit.SET_UNIT(object)
                }
                return object
            }
        },
        watch: {
            $lead: {
                handler(newValue){
                    if (newValue){
                        this.objectValue = newValue.lead
                    }
                },
                deep: true,
                immediate: true
            }
        }
    })
    export default LeadPanel as typeof LeadPanel & SafeBaseComponent
</script>