import type { Id } from "entities/lead/types/index"

interface Profile{
    id: Id,
    name: string,
    leadId?: Id | null
}

interface ProfileState{
    profile: Profile | null
}

interface ProfileView{
    name: string
}

interface ProfileCreate extends ProfileView{}

interface ProfileEdit extends ProfileView{}


export type { 
    Profile, 
    ProfileState,
    ProfileView,
    ProfileCreate,
    ProfileEdit
}