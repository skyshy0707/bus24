import { createStore, type StateCreator } from "zustand/vanilla"
import { persist } from 'zustand/middleware'

import type { LeadView, LeadState } from "entities/lead/types"

const leadStore = createStore(persist(((get, set) => ({

        lead: null as LeadView | null,
            
        GET_LEAD: (): LeadView | null => {
            return leadStore.getState().lead
        },

        SET_LEAD: (lead: LeadView | null): void => {
            leadStore.setState({ lead: lead })
        }
    })) as StateCreator<LeadState & {
        GET_LEAD: () => LeadView | null,
        SET_LEAD: (lead: LeadView | null) => void
    }>,
    {
        name: 'bus-lead-storage', // Ключ в localStorage
    }
))

export default leadStore