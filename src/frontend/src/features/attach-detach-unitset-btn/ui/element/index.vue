<template>
    <button 
        @click="toExternalComponent"
        type="button"
        :class="getClassBtn()"
    >
        {{ button_send_set }}
    </button>
</template>


<style lang="css">
    .minus-items{
        background-color: rgba(104, 0, 0, 0.555);
        border-radius: 15%;
        width: 90px
    }
    .plus-items {
        background-color: #00501b77;
        border-radius: 15%;
        width: 90px
    }
</style>
<script lang="ts">

    import { defineComponent, type PropType } from 'vue'

    import type { Id } from "@shared/types/types"

    export default defineComponent({
        inheritAttrs: false,
        props: {
            set: {
                type: Array as PropType<Id[]>
            },
            change_type: {
                type: String as PropType<'add' | 'remove'>
            },
            button_send_set: {
                type: String as PropType<string>
            },
            where_emit: {
                type: String as PropType<string>
            }
        },
        methods: {        
            async toExternalComponent(event: Event){
                event.preventDefault()
                console.log(`SendSet.toExternalComponent: ${this.set}`)
                console.log(`where emit: ${this.where_emit}`)

           
                this.$emit(this.where_emit, {
                    change_type: this.change_type,
                    units: this.set
                })
            },
            getClassBtn(){
                return this.button_send_set == '🚌➕' ? 'plus-items' : 'minus-items'
            }
        },
        watch: {
            set: {
                handler(newPropValue){
                    if (newPropValue) {
                         console.log(`updated prop \/set\/ was sended to SendSet: ${newPropValue}`)
                    }
                }
            }
        }
    })
</script>