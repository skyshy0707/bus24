<template>

    <div>
        <button
            v-if="addNew"
            class="switch-btn"
            type="button"
            @click="() => switchUiModel()"
        >
            +
        </button>
        <FormModel>
            <form 
                v-if="form"
                class="form-model"
                @submit.prevent="async ($event) => { await action($event) }"
            >
                <component
                    class="model"
                    :is="getComponentByModel(crudModel.model)"
                    v-model:object="objectValue"
                    :actionType="actionTypeValue"
                >
                </component>
                <button 
                    v-if="actionTypeValue != undefined && ['edit', 'view'].includes(actionTypeValue) && isOwn()" 
                    @click="() => actionTypeValue = actionTypeValue == 'edit' ? 'view' : 'edit'" 
                    type="button"
                    class="action-btn"
                >✏️ EDIT
                </button>
                <button 
                    v-if="actionTypeValue == 'edit' && isOwn()"
                    type="submit"
                    class="apply-btn"
                    :disabled="isEqual(objectValue, printObject)"
                >✔️ APPLY
                </button>
                <button
                    v-if="actionTypeValue != 'create' && isOwn()"
                    @click="() => DELETE(objectValue.id)"
                    type="button"
                    class="action-btn"
                >❌ DELETE
                </button>
                <button
                    v-if="actionTypeValue == 'create' && addNew"
                    type="submit"
                    class="action-btn"
                >💾 SAVE
                </button>
            </form>
        </FormModel>
        <p
            v-if="error"
        >
            {{ error }}
        </p>
    </div>

    <slot />
    
</template>

<style lang="css">
  .switch-btn{
    margin: 4px
  }
</style>

<script lang="ts">
    import { defineComponent, type PropType } from 'vue'

    import { useLocalStorage } from "@vueuse/core"

    import { getComponentByModel } from "entities/model_component/lib/component/component"
    import { Crud } from "@shared/model/crud"
    import type { CrudModel } from "@shared/types/interfaces"
    import { FormModel } from "@shared/ui/themes"
    import type { Id, Item, Response } from "@shared/types/types"
    import * as validators from "@shared/types/validators"
    import { isEqual } from "@shared/lib/format"

    import { type CrudParams } from "entities/model_component/types"

    export default defineComponent({
        components: {
            FormModel,
        },
        data() {
            return {
                printObject: { ...this.object },
                formInit: '',
                actionTypeValue: this.actionType,
                getComponentByModel,
                isEqual,
                objectValue: { ...this.object },
                error: ''
            }
        },
        mounted(){
            if (!this.objectValue.id){
                this.form = false
            }
            else this.form = useLocalStorage(`formModelComponent${this.crudModel.model}`, false)
        },
        updated(){
            if (this.objectValue.id != undefined){
                this.form = true
            }
        },
        inject: [
            '$profile',
            '$user'
        ],
        props: {
            actionType: {
                type: String as PropType<string>,
                validator: validators.actionType
            },
            object: {
                type: Object as PropType<Item>,
                required: true
            },
            crudModel: {
                type: Object as PropType<CrudModel>,
                required: true
            }
        },
        computed: {
            api(){
                return new Crud(this.crudModel)
            },
            addNew(){
                if (this.$user.token && !this.$profile.profile && this.crudModel.model == 'profile'){
                    return true
                }
                if (this.$user.token && this.$profile.profile && this.crudModel.model != 'profile'){
                    return true
                }
                return false
            },
            form: {
                get(){
                    return this.formInit
                },
                set(value: boolean){
                    this.formInit = value
                }
            }
        },
        watch: {
            object: {
                handler(newPropValue){
                    if (newPropValue){
                        this.objectValue = { ...newPropValue }
                        this.printObject = { ...newPropValue }
                        if (!isEqual(this.objectValue, this.api.model.defaultObject) && this.actionTypeValue == 'create'){
                            this.actionTypeValue = 'edit'
                        }
                    }
                },
                immediate: true
            },
            objectValue: {
                handler(updated){
                    this.objectValue = updated
                    this.$emit('update:object', { ...updated})
                },
                deep: true
            },
            actionType: {
                handler(newPropValue){
                    if (newPropValue){
                        this.actionTypeValue = newPropValue
                    }
                },
                deep: true
            }
        },
        methods: {
            isOwn(){
                if (this.api.model.model == 'profile'){
                    return this.objectValue.id == this.$profile.profile?.id
                }
                return this.objectValue.atp_id == this.$profile.profile?.id || this.objectValue.atp == this.$profile.profile?.id
            },
            switchUiModel(){
                this.form = !this.form
                this.objectValue = this.api.model.defaultObject
                this.actionTypeValue = 'create'
            },
            async executeCrudAction(actionType: 'edit' | 'create' | 'delete', params: CrudParams) {
                this.error = "";
            
                const crud = {
                    edit: {
                        successCode: 200,
                        reset: (data: any) => {
                            this.objectValue = { ...data };
                            this.printObject = { ...data };
                        },
                        method: async (params: CrudParams): Promise<Response>  => {
                            const id = params.id
                            const formdata = params.formdata
                            return await this.api.edit(formdata, id)
                        }
                    },
                    create: {
                        successCode: 201,
                        reset: (data: any) => {
                            this.objectValue = { ...data };
                            this.printObject = { ...data };
                            this.actionTypeValue = 'edit';
                        },
                        method: async (params: CrudParams): Promise<Response>  => {
                            const formdata = params.formdata
                            return await this.api.create(formdata)
                        }
                    },
                    delete: {
                        successCode: 204,
                        reset: () => {
                            this.objectValue = this.api.model.defaultObject;
                        },
                        method: async (params: CrudParams): Promise<Response> => {
                            const id = params.id
                            return await this.api.delete(id)
                        }
                    }
                };

                try {
                    const method = crud[actionType].method;

                    const response = await method(params)

                    const status = response.status || response.response_status;
                    const currentStrategy = crud[actionType];

                    if (status !== currentStrategy.successCode) {
                        this.error = response.data?.detail || response.statusText;
                        return response;
                    }

                    currentStrategy.reset(response.data);
                    return response;

                } 
                catch (err: any) {
                    this.error = err.message || "Network error";
                }
            },
            async EDIT(event: Event) {
                event.preventDefault()
                this.actionTypeValue = 'edit'
                this.form = true
                const formData = new FormData(event.target as HTMLFormElement)

                await this.executeCrudAction(
                    'edit', { 
                        id: this.objectValue.id, 
                        formdata: formData 
                    }
                )
            },
            async DELETE(id: Id){
                await this.executeCrudAction('delete', { id: id })
            
            },
            async CREATE(event: Event){
                const formData = new FormData(event.target as HTMLFormElement)
                await this.executeCrudAction('create', { formdata: formData })
            },
            async action(event: Event){
                if (this.actionTypeValue == 'edit') {
                    return await this.EDIT(event)
                }
                else if (this.actionTypeValue == 'create') {
                    await this.CREATE(event)
                }
            }
        }
    })
</script>