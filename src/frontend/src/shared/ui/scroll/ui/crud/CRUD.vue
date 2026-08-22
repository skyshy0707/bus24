<template>
    <div
        class="actions"
    >
        <template
            v-if="itemView"
        >
            <button
                class="btn"
                v-if="isLink(item[itemView.fieldName])"
                @click="() => to(item[(itemView as ItemView).fieldName])"
                role="button"
            >
                {{ itemView?.description ? itemView.description : '🌍 SOURCE' }}
            </button>
        </template>
        <button 
            class="btn"
            v-if="enabledSubset"
            type="button"
            @click="() => moveToChangeSet(item.id)"
        >
            {{ setSymbolToElement }}
        </button>
        <button
            class="btn detail-btn"
            type="button"
            @click="() => view((item as Item).id)"
        >
            {{ itemView?.icon ? itemView.icon : '' }} {{ itemView && !isLink(item[itemView.fieldName]) ? standardtize(item[itemView.fieldName]) : '' }} DETAIL 
        </button>
        <button
            class="btn"
            v-if="item.atp_id == $profile?.profile?.id || item.atp == $profile?.profile?.id"
            type="button"
            @click="() => delete_((item as Item).id)"
        >
            ❌ DELETE
        </button>
    </div>
</template>

<script lang="ts">

import { defineComponent, type PropType } from 'vue'

import { to } from "@shared/api/schema/requests"
import type { ItemView } from "@shared/types/interfaces"
import { BaseCrud } from "@shared/ui/scroll/ui/base"
import type { Id, Item } from "@shared/types/types"

const CRUD = defineComponent({
    name: 'CRUD',
    mixins: [BaseCrud as any],
    inject: {
        $profile: {
            from: '$profile',
            default: () => null as any
        }
    },
    data(){
        return {
            to,
            copySet: this.set
        }
    },
    props: {
        enabledSubset: {
            type: Boolean as PropType<boolean>,
            default: false
        },
        item: {
            type: Object as PropType<Item>,
            required: true
        },
        items: {
            type: Array<Item> as PropType<Array<Item>>
        },
        itemView: {
            type: Object as PropType<ItemView>
        },
    },
    computed: {
        setSymbolToElement(){
            if (this.mark_element_action_as === 'add'){
                return '➕'
            }
            else return '➖'
        },
    },
    methods: {
        isLink(link: any){
            return typeof link == 'string' ? link.includes('://') : false
        },
        standardtize(value: string | number){
            const maxR = 4
            const r = typeof value == 'number' ? String(value).length : value.length
            
            if (r > maxR){
                value = value.toString().slice(0, maxR-2) + '..'
            }

            for (let i=0; i < maxR - r; i++){
                value = '\u2003' + value
            }
            return value
        },
        moveToChangeSet(id: Id){
            const reduced = this.getReducedSet(id, this.items)
            const changeSet = [...this.copySet, id]
            this.copySet = changeSet
            
            this.$emit('update:items', JSON.parse(JSON.stringify(reduced)))
            this.$emit('update:set', JSON.parse(JSON.stringify(changeSet)))
        },
    },
    
})


export default CRUD as typeof CRUD & typeof BaseCrud
</script>