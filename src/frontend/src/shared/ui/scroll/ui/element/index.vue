
<template>
    <div
        @scroll="loadFromServer"
    >
        <div>
            <div
                v-if="contentDraw"
                class="scroll-content select-from-list"
                @scroll="loadFromServer"
            >
                <template
                    v-if="contentDraw"
                >
                    <div 
                        class="list"
                        v-for="item in items" :key="item.id"
                    >
                        <div 
                            v-for="(label, fieldName) in labels"
                            :key="fieldName"
                        >
                            <div
                                v-if="item[fieldName] != item.value"
                                class="field-radio"
                            >
                                <strong >
                                    {{ label }}:
                                </strong>
                                <span 
                                    v-if="labels !== undefined"
                                >
                                    {{ dateOrAny(item[fieldName]) }}
                                </span>
                            </div>
                        </div>
                        <template
                            v-if="selectDraw"
                        >
                            <label>
                                <input
                                    :type="selectType"
                                    :name="(select as Select).fieldName"
                                    :value="item.id"
                                    v-model="selectedValue"
                                    @input="$emit('on-input', $event)"
                                />
                                {{ item.value }}
                            </label>
                        </template>
                        <template
                            v-if="enabledCrud"
                        >
                            <CRUD
                                v-if="item !== undefined"
                                :enabledSubset="enabledSubset"
                                :mark_element_action_as="mark_element_action_as"
                                :item="item"
                                v-model:items="items"
                                :itemView="itemView"
                                :set="copySet"
                                @updateItems="(id: Id) => updateItems(id)"
                                @update:set="(newValue) => updateSet(newValue)"
                                @delete="delete_"
                                @get="view"
                            >
                            </CRUD>
                        </template>
                    </div>
                </template>
              
            </div>
            
            

            <div 
                class="item-crud"
                @scroll="loadFromServer"
                v-if="enabledCrud && !contentDraw"
            >

                <template
                    v-for="item in items" :key="item.id"
                >   
                    <CRUD
                        v-if="item !== undefined"
                        :enabledSubset="enabledSubset"
                        :mark_element_action_as="mark_element_action_as"
                        :item="item"
                        v-model:items="items"
                        :itemView="itemView"
                        :set="copySet"
                        @update:set="(newValue) => updateSet(newValue)"
                        @updateItems="(id: Id) => updateItems(id)"
                        @delete="delete_"
                        @get="view"
                    >
                    </CRUD>
                </template>
            </div>
        </div>
    </div>

    <div 
        v-if="enabledSubset"
    >
        <div
            class="subsetPlus"
        >
            <button
                v-for="id in copySet" :key="id"
                type="button"
                @click="() => removeFromChangeSet(id)"
                :class="setClassPrefixToSet + '-items'"
            >
                {{ setSymbolToSet }}🚍: {{ id }}
            </button>
        </div>
    </div>

    <slot />

</template>

<style lang="css">

.actions{
    margin: 2px;
    flex-direction: row; 
    display: flex;
}

.btn {
    margin: 2px;
    border-radius: 4px
}

.detail-btn {
    font-family: ui-monospace, SFMono-Regular, monospace; 
    white-space: pre
}

.add-items, .remove-items{
    width: 90px;
    border-radius: 15%;
    background-color: rgba(255, 0, 0, 0.6);
}

.add-items{
    background-color: rgba(255, 0, 0, 0.6);
}

.remove-items{
    background-color: rgba(0, 99, 5, 0.6);
}


.field-radio {
    margin-bottom: 0.4em;
    margin-left: 0.5em
}

.item-crud {
    flex-direction: column; 
    display: flex; 
    overflow-y: scroll; 
    height: 100px;
}

.subsetPlus{
    height: "50px";
    grid-column: auto;
    flex-direction: column; 
    margin-top: 1.5em
}

.scroll-content{
    overflow-y: scroll; 
    width: 256px
 }


.select-from-list {
    height: 100px;
}

.list {
    flex-direction: column;
}
</style>

<script lang="ts">

    import { defineComponent, type PropType } from 'vue'

    import { parseDate } from "@shared/lib/format"
    import { request, to } from "@shared/api/schema/requests"
    import { getWsUrl } from "@shared/api/schema/api"
    import type { Select, ItemView, WSRequestParams } from "@shared/types/interfaces"
    import type { Id, Item } from "@shared/types/types"
    import { BaseCrud } from "@shared/ui/scroll/ui/base"
    import { CRUD } from "@shared/ui/scroll/ui/crud"

    
    const Scroll = defineComponent({
        name: 'Scroll',
        mixins: [BaseCrud as any],
        components: { CRUD },
        inheritAttrs: false,
        inject: {
            $profile: {
                from: '$profile',
                default: () => null as any
            }
        },
        props: {
            limit: {
                type: Number as PropType<number>,
                default: 6
            },
            endpoint: { 
                type: String as PropType<string>,
                required: true
            },
            enabledCrud: {
                type: Boolean as PropType<boolean>,
                default: false
            },
            enabledSubset: {
                type: Boolean as PropType<boolean>,
                default: false
            },
            labels: {
                type: Object as PropType<Record<string, string>>
            },
            select: {
                type: Object as PropType<Select>
            },
            object: {
                type: Object as PropType<Item>,
                default: () => { id: -1 }
            },
            itemView: {
                type: Object as PropType<ItemView>
            },
            ws: {
                type: Object as PropType<WSRequestParams>,
            }
        },
        data(){
            return {
                parseDate,
                to,
                hasMore: true,
                offset: 0,
                loading: true,
                items: [] as Array<Item>,
                copyItems: [] as Array<Item>, 
            }
        },
        computed: {
            contentDraw(): boolean { 
                if (this.labels === undefined){
                    return false
                }
                return true
            },
            multiselectName(){
                return `list-${this.model}`
            },
            selectDraw(): boolean {
                return this.select && typeof this.select == 'object' ? Object.keys(this.select).length > 0 : false
            },
            selectType(){
                return String(this.select?.selectType)=='single' ? 'radio' : 'checkbox'
            },
            setSymbolToSet(){
                return this.mark_element_action_as === 'add' ? '➖' : '➕'
            },
            setClassPrefixToSet(){
                return this.mark_element_action_as === 'add' ? 'remove' : 'add'
            },
            selectedValue: {
                get(){
                    var selected = this.object[this.select?.fieldName]

                    if (selected == undefined){
                        const key = this.select.fieldName.split('_')[0]
                        selected = this.object[key]
                    }
                    if(typeof selected == 'object' && !selected.hasOwnProperty('length')){
                        return selected.id
                    }
                    return selected
                },
                set(newValue){
                    const fieldName = (this.select as Select).fieldName
                    if (typeof this.object[fieldName] == 'object' && !this.object[fieldName].hasOwnProperty('length')){
                        this.object[fieldName] = { 
                            ...this.object[fieldName],
                            id: newValue 
                        }
                        return
                    }
                    this.object[fieldName] = newValue
                }
            }
        },

        async mounted(){
            await this.loadFromServer()
            const offset = 0

            if (this.ws){

                const last = this.items[0]
                const lastId = last ? last.id : 0
                const wsRequestParams = this.ws as WSRequestParams
                const ws = new WebSocket(getWsUrl(this.endpoint))
                
                ws.send(JSON.stringify({
                    stream: wsRequestParams.stream,                    
                    payload: {
                        action: wsRequestParams.payloadAction,
                        data: wsRequestParams.data,
                        queryParams: {
                            ...wsRequestParams.queryParams,
                            offset: offset
                        },
                        pathParams: {
                            ...(
                                wsRequestParams.pathParams ? 
                                wsRequestParams.pathParams : {}
                            )
                        }
                    }
                }))

                ws.onmessage = (event) => {
                    const items = JSON.parse(event.data.results)
                    for (let item of items){
                        if(item.id <= lastId){
                            break
                        }
                        this.items.unshift(item)
                        break
                    }
                }
            }
            
        },
        watch: {
            endpoint: {
                handler(newPropValue){
                    if (newPropValue){
                        this.items = []
                        this.copyItems = []
                        this.copySet = []
                        this.hasMore = true
                        this.loading = true
                        this.offset = 0
                        this.loadFromServer()
                    }
                }
            }
        },
        created(){
            if (this.select){
                console.log(`fieldname: ${this.object[this.select?.fieldName]}`)
            }
            
        },
        methods: {
            dateOrAny(value: any){
                if (typeof value === "string" && !value.startsWith("GMT")){
                    var date = new Date(value)
                    if ((date as Object) != 'Invalid Date' && date.toISOString().slice(0, 18) == value.slice(0, 18)){
                        return parseDate(value)
                    }
                    return value
                }
                return value
            },
            removeFromChangeSet(id: Id){
                const reduced = this.getReducedSet(id, this.copySet)
                this.copySet = reduced
                this.$emit('update:set', reduced)
                const item: Item = this.copyItems.find(item => item.id == id)
                this.items.push(item)
                
            },
            async loadFromServer(){
                if (!this.hasMore || !this.loading) return
                this.loading = false
                const response = await request({
                    url: this.endpoint,
                    params: {
                        limit: this.limit,
                        offset: this.offset
                    }
                })
                const items = response.data ? response.data.results || []: []

                if (items.length === 0){
                    this.hasMore = false
                    this.loading = false
                }
                else {
                    this.items.push(...items)
                    this.copyItems.push(...items)
                    this.offset += this.limit
                    this.loading = true
                }
            },
            updateSet(newValue: Array<Item>){
                this.$emit('update:set', [...newValue]) 
                this.copySet = [...newValue]
            },
            updateItems(id: Id){
                //console.log(`launch update items: ${id}`)
                console.log(`items typeof: ${typeof this.items}`)
                this.items = this.getReducedSet(id, this.items)
            }
        }
    })
    export default Scroll as typeof Scroll & typeof BaseCrud

</script>