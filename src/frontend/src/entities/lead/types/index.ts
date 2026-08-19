import type { Id } from "@shared/types/types"


interface Lead{
    route_no: string
    route_wiki_url: string
    capacity_class: string
    units_per_route: number
    date: string
}


interface LeadView extends Lead{
    id: Id
    atp_id: Id
}

interface LeadEdit {
    route_no: string
    route_wiki_url: string
    capacity_class: string
    units_per_route: number
}

interface LeadCreate extends LeadEdit{}


interface LeadState {
    lead: LeadView | null
}


export type { 
    Lead, 
    LeadEdit, 
    LeadView, 
    LeadCreate, 
    Id,
    LeadState
}