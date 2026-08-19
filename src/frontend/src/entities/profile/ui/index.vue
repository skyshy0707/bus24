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
    import store from "@shared/model/store"
    import { type DjangoErrorData } from "@shared/types/types"

    import type { ProfileView, Profile } from "entities/profile/types"
    import { getProfile } from "entities/profile/api/profile"
    import profile from "entities/profile/model/store"

    

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
