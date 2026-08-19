import { useStore } from 'vuex'

import storage from "@shared/model/store"

import type { AuthorizationHeader } from "@shared/types/interfaces"

function getAuthHeader(): AuthorizationHeader | undefined{


    if (storage.getState().token){
        return { Authorization: `Bearer ${storage.getState().token}` }
    }
}

function getWsUrl(path: string){
    return `ws://${import.meta.env.VITE_DOMAIN}/${path}`
}

export {
    getAuthHeader,
    getWsUrl
}