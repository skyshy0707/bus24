import axios from "axios"
import type { AxiosResponse } from 'axios'

import { getAuthHeader } from "@shared/api/schema/api"
import { empty } from "@shared/model/constants"
import storage from "@shared/model/store"
import type { AuthorizationHeader, WSRequest } from "@shared/types/interfaces"
import type { Response } from "@shared/types/types"


async function refreshToken(){

    const response = await request(
        { 
            url: "refresh-token",
            headers: {
                Authorization: `Bearer ${storage.getState().refreshToken}`
            },
            method: "POST",
            auth: false,
            withCredentials: true
        }
    )

    if (response.status === 201){
        storage.getState().SET_TOKEN(response.data.token)
        storage.getState().SET_REFRESH_TOKEN(response.data.refresh_token)
    }
    else {
        storage.getState().DELETE_TOKEN()
    }
}

function getHeaders(auth: boolean, headers?: AuthorizationHeader & Record<string, string> | undefined){
    const deviceMemory = (navigator as any).deviceMemory
    return {
        "Content-Type": "application/json",
        "X-Sec-CH-Device-Memory": deviceMemory ? deviceMemory.toString() : '',
        ...(headers ? headers : empty), 
        ...(auth ? getAuthHeader() : empty) 
    }
}

async function request(
    {
        url, 
        method="GET",
        data=empty, 
        params=empty,
        headers=undefined as AuthorizationHeader & Record<string, string> | undefined,
        auth=true,
        withCredentials=false
    }
): Promise<Response>{
    const baseUrl = import.meta.env.VITE_API_URL


    const headersAsObject =  getHeaders(auth, headers)

    console.log(`AT REQUEST ${url} DEVICE_MEMORY: ${headersAsObject["X-Sec-CH-Device-Memory"]}`)
    
    const response: AxiosResponse = await axios({
        method: method,
        url: `${baseUrl}/${url}`,
        data: data,
        params: params,
        headers: headersAsObject != empty ? headersAsObject : undefined,
        validateStatus: function (status: number) {
            return status < 500; 
        },
        withCredentials: withCredentials ? true : (auth ? true : false)
    })

    if (response.status === 403 && response.data?.detail == "Token is expired"){
        await refreshToken()
        return await request({
            url, 
            method, 
            data, 
            params, 
            headers, 
            auth
        })
    }
    return response
}

function to(link: string){
    window.location.href = link
}

// Get client IP using WebRTC
// This is needed because WebSocket handshake goes through nginx proxy
// and client IP in scope is the proxy IP, not the real user IP
async function getClientIP(): Promise<string> {
    return new Promise((resolve, reject) => {
        const peerConnection = new RTCPeerConnection({
            iceServers: []
        })
        
        peerConnection.createDataChannel('')
        peerConnection.createOffer()
            .then(offer => peerConnection.setLocalDescription(offer))
            .catch(reject)
        
        peerConnection.onicecandidate = (event) => {
            if (!event || !event.candidate) {
                peerConnection.close()
                return
            }
            
            const candidate = event.candidate.candidate
            const ipMatch = candidate.match(/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/)
            
            if (ipMatch) {
                peerConnection.close()
                resolve(ipMatch[1])
            }
        }
        
        setTimeout(() => {
            peerConnection.close()
            reject(new Error('IP detection timeout'))
        }, 0)
    })
}

async function wsRequest({
    socket, 
    stream, 
    payloadAction, 
    auth=true,
    data, 
    headers=undefined as AuthorizationHeader & Record<string, string> | undefined,
    queryParams,
    pathParams
}: WSRequest){

    const headersAsObject = getHeaders(auth, headers)
    
    // Add device fingerprint headers from browser
    // These are captured from navigator object and sent with each request
    // because WebSocket handshake headers are replaced by nginx proxy
    if (auth) {
        const userAgent = navigator.userAgent
        headersAsObject['X-User-Agent'] = userAgent
        
        // Add device memory only if available (not 'unknown')
        const deviceMemory = (navigator as any).deviceMemory
        if (deviceMemory) {
            headersAsObject['X-Sec-CH-Device-Memory'] = deviceMemory.toString()
        }
        
        // Get real client IP via WebRTC
        try {
            const clientIP = await getClientIP()
            headersAsObject['X-Client-IP'] = clientIP
        } catch (error) {
            console.warn('Failed to get client IP:', error)
        }
    }

    return new Promise((resolve, reject) => {
        const requestId = crypto.randomUUID()

        const action = stream.split(':').pop()

        if (!payloadAction && action){
            payloadAction = action
        }

        if (!socket){
            reject(new Error('Socket was not provided'))
            return
        }

        // Check if socket is ready
        if (socket.readyState !== WebSocket.OPEN) {
            reject(new Error(`WebSocket is not open. Ready state: ${socket.readyState}`))
            return
        }

        const messageHandler = (event) => {
            try {
                const response = JSON.parse(event.data)
                console.log('Received response:', response)

                if (response.request_id === requestId) {
                    socket.removeEventListener('message', messageHandler)

                    if (response.payload?.errors || 
                        response.payload?.status && response.payload.status >= 400) {
                        console.log(`
                            errors: ${response.payload?.errors}, 
                            ${response.payload.status}`
                        )
                    }

                    resolve(response)
                }
            } catch (error) {
                console.error('Error parsing message:', error)
            }
        }

        socket.addEventListener('message', messageHandler)
        socket.addEventListener('error', (event) => { 
            console.error(`WebSocket error occur - details: ${event}`)
            reject(new Error('WebSocket error'))
        })

        const packet = {
            stream: stream,
            payload: {
                action: payloadAction,
                request_id: requestId,
                data: data,
                headers: headersAsObject,
                query_params: queryParams,
                path_params: pathParams
            }
        }
        
        // Add client IP to packet if available
        if (headersAsObject['X-Client-IP']) {
            packet.payload['client_ip'] = headersAsObject['X-Client-IP']
        }
        
        console.log(`Sending WebSocket request:`, {
            stream: packet.stream,
            action: packet.payload.action,
            requestId: packet.payload.request_id,
            data: packet.payload.data,
            headers: packet.payload.headers
        })
        
        socket.send(JSON.stringify(packet))
    })
}


export {
    request,
    to,
    wsRequest
}