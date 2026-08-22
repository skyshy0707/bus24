<template>
    <input 
        type="string" 
        name="name" 
        :disabled="actionType === 'view'" 
        v-model="objectValue.name"
        required
    />
</template>

<script lang="ts">
    import { defineComponent, type PropType } from 'vue'

    import * as validators from "@shared/types/validators"

    import type { ProfileView } from "entities/profile/types"

    export default defineComponent({

        inject: [
            '$profile'
        ],

        props: {

            actionType: {
                type: String as PropType<string>,
                validator: validators.actionType
            },
            object: {
                type: Object as PropType<ProfileView>,
                required: true
            },
        },

        data(){
            return {
                objectValue: this.object
            }
        },
        watch: {
            object: {
                handler(newPropValue){
                    if (JSON.stringify(this.objectValue) !== JSON.stringify(newPropValue)){
                        this.objectValue = { ...newPropValue }
                    }
                },
                immediate: true
            },
            objectValue: {
                handler(updated){
                    this.$emit('update:object', { ...updated })
                },
                deep: true
            }
        }
    })
</script>