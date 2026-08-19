import { createStore, type StateCreator } from "zustand/vanilla"
import { persist } from 'zustand/middleware'

import type { 
    UnitView, 
    UnitState 
} from "entities/unit/types"

const unitStore = createStore(persist(((get, set) => ({

        unit: null as UnitView | null,
    
        GET_UNIT: (): UnitView | null => {
            return unitStore.getState().unit
        },
        
        SET_UNIT: (unit: UnitView | null): void => {
            unitStore.setState({ unit: unit })
        }
    })) as StateCreator <UnitState & {
        GET_UNIT: () => UnitView | null, 
        SET_UNIT: (unit: UnitView | null) => void   
    }>,
    {
        name: 'bus-unit-storage', // Ключ в localStorage
    }
))

export default unitStore