import type { Id } from "@shared/types/types"

import type { LeadView } from "entities/lead/types"
import type { Profile } from "entities/profile/types"


interface MessageView {
    id: Id,
    atp_id: Id,
    lead: LeadView,
    to: Profile[],
    text?: string,
    date: string
}

interface MessageEdit {
    lead?: LeadView,
    text?: string
}

interface MessageCreate {
    lead: LeadView,
    to: Id[],
    text?: string
}

export type {
    MessageView,
    MessageCreate,
    MessageEdit
}