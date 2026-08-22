<template>
    <div>
        <button
            v-if="!logged"
            type="button"
            @click="() => actionTypeValue = 'signin'"
        >
            SIGNIN
        </button>
        <button
            v-if="!logged"
            type="button"
            @click="() => actionTypeValue = 'signup'"
        >
            SIGNUP
        </button>
        <button
            v-if="logged"
            type="button"
            @click="() => logout()"
        >
            LOGOUT
        </button>
    </div>
    
    
    <h5>
        {{ actionTypeValue }}
    </h5>

    <form 
        v-if="actionTypeValue"
        @submit.prevent="actionTypeValue == 'signin' ? signin($event) : signup($event)"
    >
        <input 
            name="email"
            type="email"
            :value="credentialsModel.email"
            required
        />
        <input
            name="password"
            type="password"
            :value="credentialsModel.password"
            required
        />
        <input
            v-if="actionTypeValue == 'signup'"
            name="password_2"
            type="password"
            :value="credentialsModel.password_2"
            required
        />

        <button 
            type="submit"
        >
            {{ actionTypeValue }}
        </button>
        <p 
            v-if="error"
        >
            {{ error }}
        </p>
    </form>
</template>

<script lang="ts">

import { defineComponent, type PropType, reactive } from 'vue'

import * as api from "features/credentials/api/send"
import type { Credentials, Signin, Signup } from "features/credentials/types"
import * as validators from "features/credentials/types/validators"

const defaultCredentials = reactive({
    email: "",
    password: "",
    password_2: ""
})
export default defineComponent({
    
    props: {
        credentials: {
            type: Object as PropType<Credentials>, 
            default: () => (defaultCredentials)
        },
        actionType: {
            type: String as PropType<string> | null,
            validator: validators.actionType,
        },
        logged: {
            type: Boolean as PropType<boolean>,
            required: true,
            default: false
        }
    },
    data() {
        return {
            credentialsModel: this.credentials,
            actionTypeValue: this.actionType,
            error: ""
        }
    },
    methods: {
        cleanForm(event: Event, encode=true){
            const entries = (new FormData(event.target as HTMLFormElement)).entries()
            const raw = Object.fromEntries(entries)
            for (const key in raw){
                let record = raw[key]
                if (typeof record == 'string' && encode){
                    raw[key] = btoa(raw[key] as string)
                }
            }
            return raw
        },
        async signin(event: Event){
            event.preventDefault()

            const response = await api.signin(
                (this.cleanForm(event, false) as Partial<Signin>) as Signin
            )

            if (response.status == 201){
                this.$router.push("/")
            }
            this.error = response.data.message || response.statusText
        },

        async signup(event: Event){
            event.preventDefault()
            const data = (this.cleanForm(event) as Partial<Signup>) as Signup
            const response = await api.signup(
                data
            )

            if (response.status == 201){
                this.actionTypeValue = "signin"
                this.credentialsModel = defaultCredentials
                this.error = ""
            }

            else {
                this.error = response.data.message
            }
        },
        async logout(){
            await api.logout()
        }
    }
})
</script>