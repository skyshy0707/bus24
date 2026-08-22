import { type AxiosResponse } from 'axios'

import { request } from "@shared/api/schema/requests"
import type { CrudModel } from "@shared/types/interfaces"
import type { DjangoErrorData } from "@shared/types/types"

import type { 
    Profile,
    ProfileCreate, 
    ProfileEdit
} from "entities/profile/types"

class ProfileApi implements CrudModel{

    model = 'profile'

    defaultObject: Profile = {
        id: -1,
        name: ""
    }

    async get(){

        const response  = await request({
            url: `profile`
        })

        return response
    }

    async edit(data: FormData){
        const validated = Object.fromEntries(data.entries()) as Partial<ProfileEdit>

        const response  = await request({
            url: `atp/edit`,
            data: validated,
            method: "PATCH"
        })

        return response
    }

    async create(data: FormData){

        const validated = Object.fromEntries(data.entries()) as Partial<ProfileCreate>
        const response  = await request({
            url: `atp/create`,
            data: validated,
            method: "POST"
        })

        return response
    }

    async delete(){
        const response = await request({
            url: `atp/delete`,
            method: "DELETE"
        })

        return response
    }
}

async function getProfile(): Promise<AxiosResponse<Profile | DjangoErrorData>>{

    const response: AxiosResponse<Profile | DjangoErrorData> = await request({
        url: "profile"
    })

    return response
}


export { 
    getProfile,
    ProfileApi
}