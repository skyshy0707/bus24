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
  .action-btn{
    margin: 4px;
    background-color: rgba(26, 1, 86, 0.6);
    border-radius: 15%;
    width: 90px
  }
  .apply-btn{
    margin: 4px;
    background-color: rgba(59, 58, 58, 0.6);
    border-radius: 15%;
    color: white;
    width: 90px
  }

  .form-model {
    margin: 4px;
    background-color: rgba(168, 141, 173, 0.6);
    border-radius: 10px
  }

  .model {
    padding-bottom: 0.5em;
    flex-direction: column
  }

  .model > div {
    padding-bottom: 0.5em
  }

  .model > div > div {
    padding-bottom: 0.5em;
    width: 220px
  }

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
    import type { Id, Item } from "@shared/types/types"
    import * as validators from "@shared/types/validators"
    import { isEqual } from "@shared/lib/format"

    //:object="objectValue"
    //:action-type="actionTypeValue"
    //const objectValue = makeReactive(`objectValue${this.crudModel.model}`, )
    export default defineComponent({
        components: {
            FormModel,
        },
        data() {
            console.log(`DATA  RUN`)
            return {
                printObject: { ...this.object },
                form: useLocalStorage(`formModelComponent${this.crudModel.model}`, false),
                actionTypeValue: this.actionType,
                getComponentByModel,
                isEqual,
                objectValue: { ...this.object },
                error: ''
            }
        },
        updated(){
            console.log(`UPDATED - pr.name: ${this.printObject.name}, o.name: ${this.objectValue.name}`)

            for (let key of Object.keys(this.objectValue)){
                console.log(`pr.${key}: ${this.printObject[key]}, o.${key}: ${this.objectValue[key]}`)
            }


            console.log(`UPDATED MC actionType: ${this.actionTypeValue}`)
            this.form = true
            //this.resetform()
        },
        mounted(){
            console.log(`MOUNTED MC actionType: ${this.actionTypeValue}`)
            console.log(`MOUNTED - pr.name: ${this.printObject.name}, o.name: ${this.objectValue.name}`)
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
                console.log(`token: ${this.$user.token}, profile: ${this.$profile.profile}`)
                if (this.$user.token && !this.$profile.profile && this.crudModel.model == 'profile'){
                    return true
                }
                if (this.$user.token && this.$profile.profile && this.crudModel.model != 'profile'){
                    return true
                }
                return false
            },
            resetform(){
                if (!this.$profile.profile){
                    this.form = false
                }
            },
            /*modelComponentProps(){
                return {
                    object: { ... this.objectValue },
                    actionType: this.actionTypeValue
                }
            }*/
        },
        watch: {
            object: {
                handler(newPropValue){

                    console.log(`OBJECT WATCH HANDLER LAUNCH: ${newPropValue.id}`)
                    if (newPropValue){

                        this.objectValue = { ...newPropValue }
                        this.printObject = { ...newPropValue }

                        console.log(`original actionTypeValue: ${this.actionTypeValue}`)

                        if (!isEqual(this.objectValue, this.api.model.defaultObject) && this.actionTypeValue == 'create'){
                            this.actionTypeValue = 'edit'
                        }
                    }
                },
                immediate: true
            },
            objectValue: {
                handler(updated){
                    console.log(`objectValue.updated: ${updated}`)
                    console.log(`CHECK CHANGES IN BOTH - OBJECT VALUE AND PRINT OBJECT`)
                    for (let key of Object.keys(this.objectValue)){
                        console.log(`pr.${key}: ${this.printObject[key]}, o.${key}: ${this.objectValue[key]}`)
                    }

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
                console.log(`isOwn: ${this.objectValue.id}. ${this.$profile.profile?.id}`)
                if (this.api.model.model == 'profile'){
                    return this.objectValue.id == this.$profile.profile?.id
                }
                console.log(`
                    isOwn NON PROFILE object.atp_id: ${this.objectValue.atp}. 
                    atp_id ${this.$profile.profile?.id}
                    obj.atp_id ${this.objectValue.atp_id}
                    objectValue: ${Object.keys(this.objectValue)}
                `)
                return this.objectValue.atp_id == this.$profile.profile?.id || this.objectValue.atp == this.$profile.profile?.id
            },
            switchUiModel(){
                this.form = !this.form
                this.objectValue = this.api.model.defaultObject
                this.actionTypeValue = 'create'
            },
            async EDIT(event: Event) {
                event.preventDefault()
                this.actionTypeValue = 'edit'
                this.form = true
                const formData = new FormData(event.target as HTMLFormElement)
                const response = await this.api.edit(formData, this.objectValue.id)

                console.log(`actionTypeValue after edit op: ${this.actionTypeValue}`)

                const responseStatus = response.status || response.response_status

                if (responseStatus != 200){
                    this.error = response.data?.detail || response.statusText
                    //this.objectValue = this.api.model.defaultObject
                }
                else{
                    this.objectValue = { ...response.data }
                    this.printObject = { ...response.data }
                    this.error = ""
                }

                //console.log(`EDIT.status: ${responseStatus}, object.id: ${response.data.id}`)

            },
            async DELETE(id: Id){
                const response = await this.api.delete(id)

                const responseStatus = response.status || response.response_status
                
                if (responseStatus != 204){
                    this.error = response.data?.detail || response.statusText
                }
                else{
                    this.objectValue = this.api.model.defaultObject
                    this.error = ""
                }
            },
            async CREATE(event: Event){
                const formData = new FormData(event.target as HTMLFormElement)
                const response = await this.api.create(formData)

                const responseStatus = response.status || response.response_status

                console.log(`response.status create:, ${responseStatus }`)
                if (responseStatus != 201){
                    this.error = response.data?.detail || response.statusText
                    this.form = true
                }
                else{
                    console.log(`created attrs: ${Object.keys(response.data)}`)
                    this.objectValue = { ...response.data }
                    this.printObject = { ...response.data }
                    this.error = ""
                    this.actionTypeValue = 'edit'
                }
                return response
            },
            async action(event: Event){
                console.log(`actiontype: ${this.actionTypeValue}`)
                if (this.actionTypeValue == 'edit') {
                    return await this.EDIT(event)
                }
                else if (this.actionTypeValue == 'create') {
                    console.log(`case create`)
                    const k = await this.CREATE(event)
                    console.log(`response: ${k}, ${typeof k}`)
                }
            }
        }
    })
</script>