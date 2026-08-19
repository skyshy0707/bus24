import type { Component, ExtractPropTypes } from 'vue'

import type { CrudOpResult, Id } from "@shared/types/types"

interface CrudModel {

    model: string

    defaultObject: Record<string, any>

    ws?: WebSocket | null

    create(data: FormData): Promise<CrudOpResult> | CrudOpResult

    delete(id?: Id): Promise<CrudOpResult> | CrudOpResult

    edit(data: FormData, id?: Id): Promise<CrudOpResult> | CrudOpResult

    get(id?: Id): Promise<CrudOpResult> | CrudOpResult

}

interface CrudManager {
    model: CrudModel
}


interface Select {
    selectType: 'multi' | 'single'
    fieldName: string // Имя поля в целевом объекте
}

interface ItemView {
    fieldName: string
    description?: string
    icon?: string
}

interface AuthKeys {
    token: string | null
    refreshToken: string | null
}

interface Auth {
    auth: AuthKeys
}

interface AuthorizationHeader{
    Authorization: string
}

interface Request {
    url: string
    method: string
    data?: Record<string, any>
    headers?: AuthorizationHeader & Record<string, any>
    params?: Record<string, any>
    auth: boolean
}

interface WSRequestParams {
    stream: string
    payloadAction?: string
    auth?: boolean
    data?: Record<string, any>
    headers?: AuthorizationHeader & Record<string, string>
    queryParams?: Record<string, any>
    pathParams?: Record<string, any>
}

interface WSRequest extends WSRequestParams {
    socket: WebSocket | null
}

interface SettingItem<T extends Component> {
    model: string,
    loader: () => Promise<any>,
    resolve: (module: any) => T,
    _typeProps: ExtractPropTypes<T>
}

export type {
    Auth,
    AuthKeys,
    AuthorizationHeader,
    CrudManager, 
    CrudModel,
    ItemView,
    Request,
    Select,
    SettingItem,
    WSRequest,
    WSRequestParams
}