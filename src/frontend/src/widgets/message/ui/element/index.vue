<template>


    <div class="shoutbox">

        <p>Шауты сообщений:</p>
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

    import type { CrudModel } from "@shared/types/interfaces"
    import type { Id } from "@shared/types/types"
    
    import { ATPLabels, MessageLabels } from 'entities/message/schema'
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
            async viewChat(id: Id){
                this.chat = `chat/${id}`
            }
        }

    })

    export default MessagePanel as typeof MessagePanel & SafeBaseComponent

</script>