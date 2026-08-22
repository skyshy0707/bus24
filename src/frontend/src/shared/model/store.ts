import { createStore, type StateCreator } from "zustand/vanilla"
import { persist } from 'zustand/middleware'

import type { AuthKeys } from "@shared/types/interfaces"


const store = createStore(persist(((set) => (
    {

        token: null as string | null,
        refreshToken: null as string | null,


        SET_TOKEN: (token: string) => {
            store.setState({ token: token })
        },

        SET_REFRESH_TOKEN: (token: string) => {
            store.setState({ refreshToken: token })
        },

        DELETE_TOKEN: () => {
            store.setState({ 
                token: null,
                refreshToken: null
            })
        }
    }
        
    )) as StateCreator<AuthKeys & {
        SET_TOKEN: (token: string) => void,
        SET_REFRESH_TOKEN: (token: string) => void,
        DELETE_TOKEN: () => void
    }>,
    {
        name: 'vanilla-app-storage-user', // Ключ в localStorage
    }
))

export default store