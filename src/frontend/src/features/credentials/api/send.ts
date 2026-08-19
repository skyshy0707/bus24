import { request } from "@shared/api/schema/requests"
import store from "@shared/model/store"

import type { 
    Signin, 
    Signup 
} from "features/credentials/types"

async function signup(data: Signup){
    const response = await request({
        url: "signup",
        data: data,
        method: "POST",
        auth: false
    })

    return response
}

async function signin(data: Signin){
    const authStr = `${data.email}:${data.password}`

    const response = await request({
        url: "signin",
        method: "POST",
        headers: {
            Authorization: `Basic ${btoa(authStr)}`
        },
        auth: false
    })

    if (response.status === 201){
        store.getState().SET_TOKEN(response.data.token)
        store.getState().SET_REFRESH_TOKEN(response.data.refresh_token)
    }

    return response
}

async function logout(){
    const response = await request({
        url: "logout"
    })
    if (response.status === 204){
        store.getState().DELETE_TOKEN()
        return true
    }

    console.log(`detail: ${response.data.detail}`)
    return false
}

export {
    logout,
    signin,
    signup
}

