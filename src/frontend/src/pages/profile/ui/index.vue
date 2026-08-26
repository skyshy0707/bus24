<template>

    <router-view/>

    <Wrapper>
        <sidebar>
        </sidebar>

        <div
            v-if="$user?.token"
            class="components"
        >
            <UnitPanel>
            </UnitPanel>

            <LeadPanel>
            </LeadPanel>

            <MessagePanel>
            </MessagePanel>

            <ProfilePanel
                :object="profileData"
            >
            </ProfilePanel>
        </div>
        
    </Wrapper>
    
</template>

<style lang="css">
    .components{
        display: flex;
        flex-direction: row;
    }

    .components > div {
        margin: 0.5em;
        padding-left: 2em;
    }
    @media (max-width: 1024px){
        .components{
            flex-direction: column;
        }

    }

</style>

<script lang="ts">

import { defineComponent } from 'vue'
    
import { Wrapper } from '@shared/ui/themes'

import { getProfile, ProfileApi } from 'entities/profile/api/profile'
import type { Profile } from 'entities/profile/types';
import profile from "entities/profile/model/store"

import { sidebar } from "features/sidebar"
import { LeadPanel } from "widgets/lead"
import { MessagePanel } from "widgets/message"
import { ProfilePanel } from "widgets/profile"
import { UnitPanel } from "widgets/unit"


export default defineComponent({
    components: {
        LeadPanel,
        MessagePanel,
        ProfilePanel,
        UnitPanel,
        sidebar,
        Wrapper
    }, 
    inject: {
        $user: {
            from: '$user',
            default: () => null as any
        }
    },
    data() {
        return {
            profileData: new ProfileApi().defaultObject
        }
    },
    async created(){
        this.profileData = await this.retrieveProfile()
    },
    methods: {
        async retrieveProfile(){
            const response = await getProfile()
            let profileData = null as Profile | null
            profileData = response.status == 200 ? (response.data as Profile) : null as Profile | null
            profile.getState().SET_USER_PROFILE(profileData)
            return profileData
        }
    }
})
</script>