import { defineComponent } from 'vue'

import { useStore } from "@shared/lib/reactive"
import store from "@shared/model/store"

import profile from 'entities/profile/model/store'
import leadStore from 'entities/lead/model/store'
import unitStore from 'entities/unit/model/store'


export const ProfileStore = defineComponent({
    data(){
        return {
            profile: useStore(profile),
            lead: useStore(leadStore),
            unit: useStore(unitStore),
            user: useStore(store)
        }
    },

    provide(){
        return {
            $profile: this.profile,
            $lead: this.lead,
            $unit: this.unit,
            $user: this.user
        }
    }
})