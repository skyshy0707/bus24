import { request, wsRequest } from "@shared/api/schema/requests"
import { getWsUrl } from "@shared/api/schema/api"
import type { CrudModel } from "@shared/types/interfaces"

import type { 
    Id,
} from "@shared/types/types"


import { LeadApi } from "entities/lead/api/lead"

import type { 
    MessageCreate, 
    MessageEdit,
    MessageView
} from "entities/message/types"
import { Message } from ".."



class MessageApi implements CrudModel{


    model = 'message'

    ws: WebSocket | null = null

    constructor() {
        this.initWebSocket()
    }

    initWebSocket() {
        try {
            const wsUrl = getWsUrl('ws/api/messages')
            console.log('Creating WebSocket connection to:', wsUrl)
            
            this.ws = new WebSocket(wsUrl)
            
            this.ws.onopen = (event) => {
                console.log('WEBSOCKET CONNECTED SUCCESSFULLY')
            }
            
            this.ws.onclose = (event) => {
                console.log('WEBSOCKET CLOSED:', event.code, event.reason)
            }
            
            this.ws.onerror = (error) => {
                console.error('WEBSOCKET ERROR:', error)
            }
            
            this.ws.onmessage = (event) => {
                console.log('WEBSOCKET MESSAGE RECEIVED:', event.data)
            }
        } catch (error) {
            console.error('Failed to create WebSocket:', error)
        }
    }

    defaultObject: MessageView = {
        id: -1,
        atp_id: -1,
        lead: new LeadApi().defaultObject,
        to: [],
        text: '',
        date: new Date().toISOString()
    }

    async get(id: Id){

        const response = await wsRequest({
            socket: this.ws,
            stream: "message:retrieve",
            pathParams: {
                id: id
            }
        })

        return response
    }

    async edit(data: FormData, id: number){
        const validated = Object.fromEntries(data.entries()) as Partial<MessageEdit>

   

        const response  = await wsRequest({
            socket: this.ws,
            stream: "message:update",
            data: validated,
            pathParams: {
                id: id
            }
        })

        return response
    }

    async create(data: FormData){
        const ret = data.entries()
        const validated = Object.fromEntries(ret) as Partial<MessageCreate>
       
        for (const key of new Set(data.keys())){
            
            var item = 
                typeof this.defaultObject[key] == 'object' && 
                this.defaultObject[key].hasOwnProperty('length') ? 
                data.getAll(key) : data.get(key)
            validated[key] = item
        }
        try {
            const response  = await wsRequest({
                socket: this.ws,
                stream: "message:create",
                data: validated,
            })
            
            return response
        } catch (error) {
            throw error
        }
    }

    async delete(id: Id){
        const response = await wsRequest({
            socket: this.ws,
            stream: 'message:destroy',
            pathParams: {
                id: id
            }
        })

        return response
    }
}

export {
    MessageApi
}