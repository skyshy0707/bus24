<template>

    <router-view/>

    <div
        class="wrapper"
    >
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
        
    </div>
    
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
    .wrapper {
        display: flex;
        flex-direction: row;
    }

    @media (max-width: 460px){
        .wrapper {
            flex-direction : column;
        }
    }

    @media (max-width: 1024px){
        .components{
            flex-direction: column;
        }

    }

</style>

<script lang="ts">

import { defineComponent } from 'vue'

//import { type DjangoErrorData } from "@shared/types/types"

import { sidebar } from "features/sidebar"
import { LeadPanel } from "widgets/lead"
import { MessagePanel } from "widgets/message"
import { ProfilePanel } from "widgets/profile"
import { UnitPanel } from "widgets/unit"



/*import { getProfile } from "entities/profile/api/profile"
import profile from "entities/profile/model/store"
import type { Profile } from "entities/profile/types"*/

import type { DjangoErrorData } from "@shared/types/types"
    
import { getProfile, ProfileApi } from 'entities/profile/api/profile'
import type { ProfileView, Profile } from 'entities/profile/types';
import profile from "entities/profile/model/store"

export default defineComponent({
    components: {
        LeadPanel,
        MessagePanel,
        ProfilePanel,
        UnitPanel,
        sidebar
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
        const p =  await this.retrieveProfile()
        console.log(`profile.atp: ${p.name}`)
        this.profileData = p
    },
    methods: {
        async retrieveProfile(){
            const response = await getProfile()
            console.log(`response.profile: ${response.statusText}, data: ${(response.data as DjangoErrorData)?.detail}`)
            console.log(`response.data: ${Object.keys(response.data)}, status: ${response.status}`)
            //console.log(`Profile: ${profile.getState().profile}`)
            //console.log(`Profile inject: ${this.$profile.profile}`)
            let profileData = null as Profile | null
            if (response.status == 200){
                profileData = response.data as Profile | null

                /*if (profileData){
                    for (const key of Object.keys(profileData as Profile)){
                        this.object[key as keyof ProfileView] = profileData[key as keyof Profile]
                    }
                }*/
                
                //this.object = profileData
            }
            console.log(`status: ${response.status}`)
            profile.getState().SET_USER_PROFILE(profileData)
            return profileData
        }
    }


    /*async mounted(){
        const response = await getProfile()
        console.log(`response.profile: ${response.statusText}, data: ${(response.data as DjangoErrorData)?.detail}`)
        console.log(`response.data: ${Object.keys(response.data)}, status: ${response.status}`)
        //console.log(`Profile: ${profile.getState().profile}`)
        //console.log(`Profile inject: ${this.$profile.profile}`)
        let profileData = null as Profile | null
        if (response.status == 200){
            profileData = response.data as Profile | null
        }
        console.log(`status: ${response.status}`)
        profile.getState().SET_USER_PROFILE(profileData)
    }*/
})
</script>