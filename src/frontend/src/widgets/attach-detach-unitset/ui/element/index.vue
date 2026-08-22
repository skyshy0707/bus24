<template>

    <Scroll
        :set="copySet"
        @update:set="(newValue) => updateSet(newValue)"
        :endpoint="endpoint"
        :mark_element_action_as="mark_element_action_as"
        :limit="limit"   
        :enabledSubset="true"
        :enabledCrud="enabledCrud"
        :itemView="itemView"
        @delete="delete_"
        @get="view"
        
    >
        <div
            class="busset-change-btn"
        >
            <p>Редактирование состава автобусов на маршруте:</p>
            <SendSet
                :set="copySet"
                @update:set="(newValue) => updateSet(newValue)"
                :change_type="change_type"
                :button_send_set="button_send_set"
                :where_emit="'sendSet'"
                @sendSet="sendSet"
                
            >
            </SendSet>
        </div>
    </Scroll>

</template>


<style lang='css'>
    .busset-change-btn{
        margin: 2px
    }
</style>
<script lang="ts">

import { defineComponent, type PropType } from 'vue'

import { BaseCrud } from '@shared/ui/scroll/ui/base'
import { Scroll } from '@shared/ui'
import type { ItemView } from "@shared/types/interfaces"

import { SendSet } from 'features/attach-detach-unitset-btn'
import type { ChangeUnitSetParams } from 'features/attach-detach-unitset-btn/types'


const ChangeUnitSet =  defineComponent({
    components: {
        Scroll,
        SendSet
    }, 
    extends: BaseCrud,
    emits: [
        'update:set'
    ],
    props: {
        limit: {
            type: Number as PropType<number>,
            default: 6
        },
        endpoint: { 
            type: String as PropType<string>,
            required: true
        },
        mark_element_action_as: {
            type: String as PropType<'add' | 'remove'>
        },
        change_type: {
            type: String as PropType<'add' | 'remove'>
        },
        button_send_set: {
            type: String as PropType<string>
        },
        where_emit: {
            type: String as PropType<string>
        },
        enabledCrud: {
            type: Boolean as PropType<boolean>,
            default: false
        },
        itemView: {
            type: Object as PropType<ItemView>
        }
    },
    methods: {
        updateSet(data){
            this.$emit('update:set', data)
            this.copySet = data
        },
        sendSet(data: ChangeUnitSetParams){
            this.$emit(
                this.where_emit, data
            )
        }
    }
})

export default ChangeUnitSet as typeof ChangeUnitSet & typeof BaseCrud
</script>