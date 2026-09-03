<template>
    <div
        class="auth-panel"
    >
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
    
    
    <h4
        class="action-title"
    >
        {{ actionTypeValueForm }}
    </h4>
    <FormModel>
        <form 
            v-if="actionTypeValue"
            class="form-model"
            style="height: 215px"
            @submit.prevent="actionTypeValue == 'signin' ? signin($event) : signup($event)"
        >
            <div
                class="model"
                style="flex-grow: 1; "
            >
                <div>
                    <div
                        class="model-field"
                    >
                        <span 
                            for="email"
                        >
                            E-mail:
                        </span>
                    </div>
                    <input 
                        class="model-field"
                        name="email"
                        type="email"
                        :value="credentialsModel.email"
                        required
                    />
                </div>
                <div>
                    <div
                        class="model-field"
                    >
                        <span 
                            for="password"
                        >
                            Пароль:
                        </span>
                    </div>
                    <input
                        class="model-field"
                        name="password"
                        type="password"
                        :value="credentialsModel.password"
                        required
                    />
                </div>
                <div
                    v-if="actionTypeValue == 'signup'"
                >
                    <div
                        class="model-field"
                    >
                        <span 
                            for="password2"
                        >
                            Повтор пароля:
                        </span>
                    </div>
                    <input
                        class="model-field"
                        name="password_2"
                        type="password"
                        :value="credentialsModel.password_2"
                        required
                    />
                </div>
            </div>

            <button 
                class="action-btn"
                type="submit"
                style="flex-shrink: 0; margin-top: 15px;"
            >
                {{ actionTypeValue }}
            </button>
            <p 
                v-if="error"
            >
                {{ error }}
            </p>
        </form>
    </FormModel>
</template>

<style lang="css">
    .action-title{
        margin-top: 2em
    }
    .auth-panel {
        top: 1.5em;
        left: 0;
        right: 0;
        background-color: rgb(87, 87, 87);
        position: fixed;
        max-width: 100vw;
        width: 100%;
        display: flex;
        z-index: 100
    }
    .auth-panel > button {
        margin: 0.2em 0.5em;
        background: wheat;
        font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
        border-radius: 10px
    }
</style>
<script lang="ts">

import { defineComponent, type PropType, reactive } from 'vue'

import { FormModel } from "@shared/ui/themes"

import * as api from "features/credentials/api/send"
import type { Credentials, Signin, Signup } from "features/credentials/types"
import * as validators from "features/credentials/types/validators"

const defaultCredentials = reactive({
    email: "",
    password: "",
    password_2: ""
})
export default defineComponent({
    components: {
        FormModel,
    },
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

    computed: {
        actionTypeValueForm() {
            if (!this.actionTypeValue){
                return ""
            }
            return this.actionTypeValue == 'signin' ? 'Вход' : 'Регистрация' 
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
                this.actionTypeValue = ""
                this.$router.push("/")
            }
            this.error = response.data.message || response.statusText
        },

        async signup(event: Event){
            event.preventDefault()
            const data = (this.cleanForm(event) as Partial<Signup>) as Signup
            const response = await api.signup(data)

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