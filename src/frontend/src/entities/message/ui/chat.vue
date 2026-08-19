
<!--Object.keys(object).length ? object[select?.fieldName] : object[select?.fieldName]-->
<template>
    <div
        class="scroll-container"
        style="overflow-y: scroll;"
        @scroll="loadFromServer"
    >
        <div>
            <div
                v-if="contentDraw"
                style="overflow-y: scroll; height: 50px;"
                @scroll="loadFromServer"
            >
                <template
                    v-if="contentDraw"
                >
                    <!--<p 
                        style="font-size: 1em;"
                    >Выбор {{ select?.fieldName }}:
                    </p>-->
                    <div 
                        style="flex-direction: column;"
                        v-for="item in items" :key="item.id"
                    >
                        <div 
                            v-for="(label, fieldName) in labels"
                            :key="fieldName"
                        >
                            <strong class="field-label">
                                {{ label }}:
                            </strong>
                            <span 
                                v-if="labels !== undefined"
                                class="field-value"
                            >
                                {{ item[fieldName] }}
                            </span>
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
                            <template
                                v-if="itemView"
                            >
                                <button
                                    v-if="isLink(item[itemView.fieldName])"
                                    @click="() => to(item[(itemView as ItemView).fieldName])"
                                    role="button"
                                >
                                    {{ itemView?.description ? itemView.description : '🌍 SOURCE' }}
                                </button>
                            </template>
                            <button 
                                v-if="enabledSubset"
                                type="button"
                                @click="() => moveToChangeSet(item.id)"
                            >
                                {{ setSymbolToElement }}
                            </button>
                            <button
                                style="font-family: ui-monospace, SFMono-Regular, monospace; white-space: pre"
                                type="button"
                                @click="() => view(item.id)"
                            >
                                {{ itemView?.icon ? itemView.icon : '' }} {{ itemView && !isLink(item[itemView.fieldName]) ? standardtize(item[itemView.fieldName]) : '' }} DETAIL 
                            </button>
                            <button
                                v-if="item.atp_id == $profile?.profile?.id || item.atp == $profile?.profile?.id"
                                type="button"
                                @click="() => delete_(item.id)"
                            >
                                ❌ DELETE
                            </button>
                        </template>
                    </div>
                </template>
              
            </div>
            
            

            <div 
                class="item-crud"
                style="flex-direction: column; display: flex; overflow-y: scroll; height: 50px;" 
                @scroll="loadFromServer"
                v-if="enabledCrud && !contentDraw"
            >
                <template
                    v-for="item in items" :key="item.id"
                >
                    <div
                        style="flex-direction: row; display: flex;"
                    >
                        <template
                            v-if="itemView"
                        >
                            <button
                                v-if="isLink(item[itemView.fieldName])"
                                @click="() => to(item[(itemView as ItemView).fieldName])"
                                role="button"
                            >
                                {{ itemView?.description ? itemView.description : '🌍 SOURCE' }}
                            </button>
                        </template>
                        <button 
                            v-if="enabledSubset"
                            type="button"
                            @click="() => moveToChangeSet(item.id)"
                        >
                            {{ setSymbolToElement }}
                        </button>
                        <button
                            style="font-family: ui-monospace, SFMono-Regular, monospace; white-space: pre"
                            type="button"
                            @click="() => view(item.id)"
                        >
                            {{ itemView?.icon ? itemView.icon : '' }} {{ itemView && !isLink(item[itemView.fieldName]) ? standardtize(item[itemView.fieldName]) : '' }} DETAIL 
                        </button>
                        <button
                            v-if="item.atp_id == $profile?.profile?.id || item.atp == $profile?.profile?.id"
                            type="button"
                            @click="() => delete_(item.id)"
                        >
                            ❌ DELETE
                        </button>
                    </div>
                </template>
            </div>
        </div>
    </div>

    <div 
        v-if="enabledSubset"
    >
        <div height="50px" style="grid-column: auto;">
            <button
                v-for="id in copySet" :key="id"
                type="button"
                @click="() => removeFromChangeSet(id)"
            >
                ➖🚍: {{ id }}
            </button>
        </div>
    </div>

    <slot />

</template>

<script lang="ts">

    import { defineComponent, type PropType } from 'vue'

    import { request } from "@shared/api/schema/requests"
    import { getWsUrl } from "@shared/api/schema/api"
    import type { Select, ItemView, WSRequestParams } from "@shared/types/interfaces"
    import type { Id, Item } from "@shared/types/types"
    import { BaseCrud } from "@shared/ui/scroll/ui/base"

    
    const Scroll = defineComponent({
        name: 'Scroll',
        mixins: [BaseCrud as any],
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
            mark_element_action_as: {
                type: String as PropType<'add' | 'remove'>,
                default: 'remove'
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
                hasMore: true,
                offset: 0,
                loading: true,
                items: [] as Array<Item>,
                copyItems: [] as Array<Item>, 
                copySet: this.set
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
                return Object.keys(this.select).length > 0 ? true : false
            },
            selectType(){
                return String(this.select?.selectType)=='single' ? 'radio' : 'checkbox'
            },
            setSymbolToElement(){
                if (this.mark_element_action_as === 'add'){
                    return '➕'
                }
                else return '➖'
            },
            selectedValue: {
                get(){
                    const selected = this.object[this.select?.fieldName]
                    if(typeof selected == 'object' && !selected.hasOwnProperty('length')){
                        return selected.id
                    }
                    return selected
                },
                set(newValue){
                    console.log(`selectedValue - newvalue: ${newValue}, typeof array ${typeof newValue}: ${newValue.hasOwnProperty('length')}`)
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

            console.log(`SCROLL CREATED contentDraw: ${this.contentDraw},  endpoint: ${this.endpoint}`)
            await this.loadFromServer()

            const offset = 0

            if (this.ws){

                const wsRequestParams = this.ws as WSRequestParams

                const ws = new WebSocket(getWsUrl(this.endpoint))

                const last = this.items[0]
                var lastId = 0

                if(last){
                    lastId = last.id
                }

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
            set: {
                handler(newPropValue){
                    if (newPropValue){
                        this.copySet = newPropValue
                    }
                },
                immediate: true
            },
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
            isLink(link: any){
                return typeof link == 'string' ? link.includes('://') : false
            },
            to(link: string){
                window.location.href = link
            },
            standardtize(bort: string | number){
                const maxR = 4
                const r = typeof bort == 'number' ? String(bort).length : bort.length
                
                if (r > maxR){
                    bort = bort.toString().slice(0, maxR-2) + '..'
                }
    
                for (let i=0; i < maxR - r; i++){
                    bort = '\u2003' + bort
                }
                return bort
            },
            moveToChangeSet(id: Id){

                console.log(`item id move to set: ${id}`)
                console.log(`items before deleting: ${this.items.length}`)
                const reduced = this.getReducedSet(id, this.items)
                console.log(`reduced items: ${reduced}`)

                this.items = reduced

                console.log(`items after deleting: ${this.items.length}`)

                //this.$emit('update:set', [...this.set, id])

                console.log(`copySet.length: ${this.copySet.length}`)
                this.copySet = [...this.copySet, id]
                this.$emit('update:set', JSON.parse(JSON.stringify(this.copySet)))
                console.log(`extended this.set: ${this.copySet}`)
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

                console.log(`response.status: ${response.status}`)

                console.log(`List response: ${Object.keys(response.data)}`)
                //console.log(`First item: id: ${response.data[1].id}, value: ${response.data[1].value}, typeof null: ${response.data[1] == null}`)
                console.log(`
                    results: ${response.data.results}, 
                    length: ${response.data?.results?.length},
                    offset: ${this.offset}
                `)

                

                const items = response.data ? response.data.results || []: []

                console.log(`count: ${response.data.count}`)

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

                if (this.items.length > 0){
                    console.log(`${Object.keys(this.items[0])}`)
                }

                
            }
        }
    })
    export default Scroll as typeof Scroll & typeof BaseCrud

</script>