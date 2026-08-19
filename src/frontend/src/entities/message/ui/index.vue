<template>
    <div>
        <div>
            <div
                v-if="actionType == 'edit' || actionType == 'create'"
                class="model-field"
            >
                <span 
                    for="lead"
                >
                    Приложить заявку:
                </span>
            </div>
            <Scroll
                v-if="actionType == 'edit' || actionType == 'create'"
                @on-input="changeCC"
                :endpoint="'uncovered-leads'"
                :labels="LeadLabels"
                :select="SelectLead"
                :object="object"
                v-model="object.lead.id"
            >
            </Scroll>

            <button
                v-if="actionType == 'view'"
                type="button"
                @click="viewLead(object.lead.id)"
            >
                LEAD
            </button>
        </div>
        <div
            v-if="$lead.lead"
        >
            <div
                v-if="actionType == 'create'"
                class="model-field"
            >
                <span 
                    for="to"
                >
                    Кому:
                </span>
            </div>
            <Scroll
                v-if="actionType == 'create' && cc"
                :endpoint="`atp-accepting-lead/${cc}`"
                :labels="ATPLabels"
                :model="'atp'"
                :select="SelectATP"
                :object="object"
                v-model="object.to"
            >
            </Scroll>
        </div>
        <div>
            <div
                class="model-field"
            >
                <span 
                    for="text"
                >
                    Комментарий:
                </span>
            </div>
            <textarea
                class="model-field"
                type="text" 
                name="text" 
                :disabled="actionType === 'view'"
                v-model="object.text"
            >
            </textarea> 
        </div>
        <span 
            v-if="actionType === 'edit' || actionType === 'view'" 
        >
            Создан: {{ parseDate(object.date) }}
        </span>
    </div>
</template>

<script lang="ts">
    import { defineComponent, type PropType } from 'vue'

    import { parseDate } from "@shared/lib/format"
    import type { Select } from "@shared/types/interfaces"
    import type { Id } from '@shared/types/types'
    import * as validators from "@shared/types/validators"
    import { Scroll } from "@shared/ui/scroll"

    import { LeadApi } from "entities/lead/api/lead"
    import type { MessageView } from "entities/message/types"
    import { 
        ATPLabels,
        SelectATP,
        LeadLabels,
        SelectLead
    } from "entities/message/schema"
    
    
    const leadApi = new LeadApi()
    export default defineComponent({

        components: {
            Scroll
        },

        data() {
            return {
                parseDate,
                ATPLabels,
                LeadLabels,
                SelectATP: SelectATP as Select,
                SelectLead: SelectLead as Select,
                cc: ''
            }
        },
        inject: {
            $lead: {
                from: '$lead',
                default: () => null as any
            }
        },
        props: {

            actionType: {
                type: String as PropType<string>,
                validator: validators.actionType
            },
            object: {
                type: Object as PropType<MessageView>,
                required: true
            },
        },
        methods: {
            /*async changeLead(event: Event){
                const leadId = (event.target as HTMLInputElement).value
                const leadResponse = await leadApi.get(leadId)

                console.log(`leadId: ${leadId}, leadresp.status: ${leadResponse.status}`)
                if (leadResponse.status === 200){
                    this.$lead.SET_LEAD(leadResponse.data)
                }
            },*/
            async changeCC(event: Event){
                const id = (event.target as HTMLInputElement).value

                const leadResponse = await leadApi.get(id)
                console.log(`leadId: ${id}, leadresp.status: ${leadResponse.status}`)
                if (leadResponse.status === 200){
                    this.cc = leadResponse.data?.capacity_class
                }
                console.log(`this.cc: ${this.cc}`)
            },
            async viewLead(id: Id){
                const leadResponse = await leadApi.get(id)

                console.log(`leadId: ${id}, leadresp.status: ${leadResponse.status}`)
                if (leadResponse.status === 200){
                    console.log(`leadResponse: ${leadResponse.data.id}`)
                    this.$lead.SET_LEAD(leadResponse.data)
                }
            }
        },
        /*watch: {
            object: {
                handler(newValue){
                    this.cc = newValue.lead.capacity_class
                }
            }
        }*/
    })
    
</script>