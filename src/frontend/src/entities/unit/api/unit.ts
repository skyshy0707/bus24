import { request } from "@shared/api/schema/requests"
import type { CrudModel } from "@shared/types/interfaces"
import type { Id } from "@shared/types/types"

import type { UnitView, UnitEdit, UnitCreate } from "entities/unit/types/index"


class UnitApi implements CrudModel{

    model = "unit"

    defaultObject: UnitView = {
        id: -1,
        atp_id: -1,
        lead_id: -1,
        bus: {
            id: -1,
            model: "",
            capacity: 0
        },
        bort: 0,
        color: ""
    }

    async get(id: Id){
        const response =  await request({
            url: `unit/${id}`
        })

        return response
    }

    async create(data: FormData){
        const validated = Object.fromEntries(data.entries()) as Partial<UnitCreate>
        const response = await request({
            url: `unit/create`,
            data: validated,
            method: "POST"
        })

        return response
    }

    async edit(data: FormData, id: Id, ){
        const validated = Object.fromEntries(data.entries()) as Partial<UnitEdit>
        const response = await request({
            url: `unit/${id}/edit`,
            data: validated,
            method: "PATCH"
        })
        return response
    }

    async delete(id: Id){
        const response = await request({
            url: `unit/${id}/delete`,
            method: "DELETE"
        })

        return response
    }
}

export {
    UnitApi
}