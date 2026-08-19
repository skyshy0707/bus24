import { request } from "@shared/api/schema/requests"
import type { CrudModel } from "@shared/types/interfaces"

import type { 
    Id, 
    LeadCreate, 
    LeadEdit,
    LeadView
} from "entities/lead/types"

class LeadApi implements CrudModel{


    model = 'lead'

    defaultObject: LeadView = {
        id: -1,
        atp_id: -1,
        route_no: '0',
        route_wiki_url: '',
        capacity_class: '',
        units_per_route: 0,
        date: new Date().toISOString()
    }

    async get(id: Id){

        const response  = await request({
            url: `lead/${id}`
        })

        return response
    }

    async edit(data: FormData, id: number){
        const validated = Object.fromEntries(data.entries()) as Partial<LeadEdit>

        const response  = await request({
            url: `lead/${id}/edit`,
            data: validated,
            method: "PATCH"
        })

        return response
    }

    async create(data: FormData){

        const validated = Object.fromEntries(data.entries()) as Partial<LeadCreate>
        const response  = await request({
            url: `lead/create`,
            data: validated,
            method: "POST"
        })

        return response
    }

    async delete(id: Id){
        const response = await request({
            url: `lead/${id}/delete`,
            method: "DELETE"
        })

        return response
    }
}

export {
    LeadApi
}