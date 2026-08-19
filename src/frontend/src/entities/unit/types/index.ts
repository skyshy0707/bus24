import type { Id } from "@shared/types/types"

interface Bus{
    id: Id,
    model: string,
    capacity: number
}

interface UnitEdit {
    lead_id?: Id,
    bort?: number,
    color?: string,
    bus_id?: Id
}

interface UnitView{
    id: Id,
    atp_id: Id,
    lead_id: Id,
    bus: Bus,
    bort: number,
    color: string
}


interface UnitCreate{
    lead_id: Id,
    bort: number,
    color: string
    bus_id: Id
}

interface UnitState{
    unit: UnitView | null
}


export type { 
    Bus, 
    UnitEdit, 
    UnitCreate,
    UnitView,
    UnitState
}