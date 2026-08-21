import { defineComponent, type PropType } from 'vue'

import { capitalize } from "@shared/lib/format"
import type { Id, Item } from "@shared/types/types"


export const BaseCrud = defineComponent({
    name: 'BaseCrud',
    inheritAttrs: false,
    emits: [
        'update:set'
    ],
    data(){
        return {
            copySet: this.set
        }
    },
    props: {
        set: {
            type: Array as PropType<Id[]>,
            default: () => []
        },
        model: {
            type: String as PropType<string>
        },
        mark_element_action_as: {
            type: String as PropType<'add' | 'remove'>,
            default: 'remove'
        },

    },
    methods: {

        getReducedSet(id: Id, set: Array<Item> | Array<Id>){
            return set.filter((item: Item | Id) => 
                (item as Item).id !== undefined ? (item as Item).id != id : item != id
            )
        },
        view(id: Id){
            console.log(`which view: ${this.model} and id: ${id}`)
            this.model ? 
                this.$emit(`get${capitalize(this.model)}`, id) : 
                    this.$emit(`get`, id)
        },
        delete_(id: Id){
            this.model ? 
                this.$emit(`delete${capitalize(this.model)}`) : 
                    this.$emit(`delete_`, id)

            const reduced = this.getReducedSet(id, this.set)
            this.copySet = reduced
            this.$emit('update:set', [...reduced])
        }
    },
    watch: {
        set: {
            handler(newValue){
                if (newValue){
                    this.copySet = newValue
                }
            },
            deep: true,
            immediate: true
        }
    }
})