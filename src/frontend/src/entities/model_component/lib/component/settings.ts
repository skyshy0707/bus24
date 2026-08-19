import type { ExtractPropTypes } from 'vue'
import { Lead } from "entities/lead"
import { Message } from "entities/message"
import { Profile } from "entities/profile"
import { Unit } from "entities/unit"


async function toDefaultImport<T>(importPromise: Promise<T>, exportName: keyof T){
    return importPromise.then(module => ({ default: module[exportName as any] }))
}

export const settings = [
    {
        model: 'lead',
        loader: () => import("../../../lead").then(module => module.Lead),
        _typeProps: {} as ExtractPropTypes<typeof Lead>
    },
    {
        model: 'message',
        loader: () => import("../../../message").then(module => module.Message),
        _typeProps: {} as ExtractPropTypes<typeof Message>
    },
    {
        model: 'profile',
        loader: () => import("../../../profile").then(module => module.Profile),
        _typeProps: {} as ExtractPropTypes<typeof Profile>
    },
    {
        model: 'unit',
        loader: () => import("../../../unit").then(module => module.Unit),
        _typeProps: {} as ExtractPropTypes<typeof Unit>
    }
]