<template>


    <div class="shoutbox">

        <p>Шаут:</p>
        <Scroll
            :endpoint="'chats'"
            :enabledCrud="true"
            :labels="ATPLabels"
            @get="viewChat"
        >
        </Scroll>

        <ModelComponent
            :actionType="actionTypeValue"
            :object="objectValue"
            :crudModel="messageApi"
            v-model="objectValue"
        >
        </ModelComponent>
        

        <div
            v-if="chat"
            class=""
        >
            <Scroll
                :endpoint="chat"
                :enabledCrud="true"
                :labels="MessageLabels"
                :itemView="itemView"
                @delete="delete_"
                @get="view"
            >

            </Scroll>
        </div>
    </div>

    



</template>

<script lang="ts">

    import { defineComponent, type PropType, reactive } from 'vue'

    import type { Id, Item } from "@shared/types/types"
    import type { CrudModel } from "@shared/types/interfaces"

    import { ATPLabels, MessageLabels } from 'entities/message/schema'
    import { LeadApi } from 'entities/lead/api/lead'
    import { MessageApi } from 'entities/message/api'
    import type { MessageView } from 'entities/message/types'
    import { ProfileStore } from 'entities/profile/ui/Profile'

    import { ModelControlPanel } from "widgets/model-control-panel"
    import type { SafeBaseComponent } from "widgets/types"

    const messageApi = reactive(new MessageApi())

    const MessagePanel = defineComponent({

        mixins: [
            ModelControlPanel as any,
            ProfileStore as any
        ],
        props: {
        object: {
            type: Object as PropType<MessageView>,
            required: false,
            default: () => messageApi.defaultObject
            },
            crudModel: {
                type: Object as PropType<CrudModel>,
                default: () => (new MessageApi()),
                required: false
            },
        }, 

        data(){
            return {
                itemView: {
                    fieldName: 'atp_name',
                    icon: '💬'
                },
                messageApi,
                ATPLabels,
                MessageLabels,
                wsRequestParams: {
                    stream: "messages:shoutbox",
                    payloadAction: "get"
                },
                chat: ''
            }
        },
        methods: {
            /*async view(id: Id){
  
                const response = await ModelControlPanel.methods?.view?.call(this, id)
                if (response.status == 200){
                    const leadResponse = await new LeadApi().get(response.data.lead_id)
                    this.lead.SET_LEAD(leadResponse)
                }
            },*/
            async viewChat(id: Id){
                console.log(`view chat: ${id}`)
                this.chat = `chat/${id}`
            }
        }

    })

    export default MessagePanel as typeof MessagePanel & SafeBaseComponent

</script>