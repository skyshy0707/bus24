<template>

    <ModelComponent
        :actionType="actionTypeValue"
        :object="object"
        :crudModel="profileApi"
    >
    </ModelComponent>

</template>

<script lang="ts">
    import { defineComponent, type PropType, reactive } from 'vue'

    import type { CrudModel } from "@shared/types/interfaces"
    import { isEqual } from "@shared/lib/format"
    
    import { ProfileApi } from 'entities/profile/api/profile'
    import type { ProfileView } from 'entities/profile/types';
    import { ProfileStore } from 'entities/profile/ui/Profile'


    import { ModelControlPanel } from "widgets/model-control-panel"
    import type { SafeBaseComponent } from "widgets/types"
import { actionType } from '@shared/types/validators';

    
    

    const profileApi = reactive(new ProfileApi())

    const ProfilePanel = defineComponent({

        mixins: [
            ModelControlPanel as any,
            ProfileStore as any
        ],

        data(){
            return {
                profileApi,
                actionTypeValue: isEqual(this.object, this.crudModel.defaultObject) ? 'create' : 'edit'
            }
        }, 
        created(){
            console.log(`WIDGET Profile, actionTypeValue: ${this.actionTypeValue}`)
        },
        props: {
            object: {
                type: Object as PropType<ProfileView>,
                //default: () => (profileApi.defaultObject as unknown as ProfileView),
                required: true
            },
            crudModel: {
                type: Object as PropType<CrudModel>,
                default: () => (new ProfileApi()),
                required: false
            },
        }
    })
    export default ProfilePanel as typeof ProfilePanel & SafeBaseComponent
</script>