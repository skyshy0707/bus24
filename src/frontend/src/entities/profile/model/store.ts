import { createStore, type StateCreator } from "zustand/vanilla"
import { persist } from 'zustand/middleware'

import { getProfile } from "entities/profile/api/profile"
import type { Profile, ProfileState } from "entities/profile/types"

const profile = createStore(persist(((set, get) => ({

        profile: null as Profile | null,

        GET_USER_PROFILE: (): Profile | null => {
            return profile.getState().profile
        },
        UPDATE_USER_PROFILE: async () => {
            const profileResponse = await getProfile() 
            if (profileResponse.status == 200) {
                profile.setState({ profile: profileResponse.data as Profile })
            }
        },
        SET_USER_PROFILE: (profileInstance: Profile | null) => {
            profile.setState({ profile: profileInstance })
        }
    })) as StateCreator<ProfileState & {
        UPDATE_USER_PROFILE: () => Promise<void>,
        SET_USER_PROFILE: (profile: Profile | null) => void,
        GET_USER_PROFILE: () => Profile | null
    }>, 
    {
        name: 'vanilla-app-storage', // Ключ в localStorage
    }
))

export default profile