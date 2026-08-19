<template>
    <div>
        <div>
            <div
                class="model-field"
            >
                <span
                >
                    Бортовой номер:
                </span>
            </div>
            <input 
                class="model-field"
                type="text" 
                name="bort" 
                v-model="object.bort"
                :disabled="actionType === 'view'" 
                required
            />
        </div>
        <template
            v-if="actionType == 'edit' || actionType == 'create'"
        >
            <div>
                <div
                    class="model-field"
                >
                    <span
                        for="bus_id"
                    >
                        Автобусы:
                    </span>
                </div>
                <Scroll
                    :endpoint="'buses'"
                    :labels="BusLabels"
                    :select="SelectBus"
                    :object="object"
                    v-model="object.bus.id"
                >
                </Scroll>
            </div>
            <div>
                <div
                    class="model-field"
                >
                    <span
                        for="color"
                    >
                        Цвет:
                    </span>
                </div>
                <Scroll
                    :endpoint="'buses/colors'"
                    :labels="UnitColorLabels"
                    :select="SelectUnitColor"
                    :object="object"
                    v-model="object.color"
                >
                </Scroll>
            </div>
        </template>
        <template
            v-if="actionType == 'view'"
        >
            <div>
                <div
                    class="model-field"
                >
                    <span
                        for="name"
                    >
                        Модель:
                    </span>
                </div>
                <input 
                    class="model-field"
                    type="text" 
                    name="bus" 
                    :disabled="actionType === 'view'" 
                    v-model="object.bus.model"
                />
            </div>
            <div>
                <div
                    class="model-field"
                >
                    <span
                        for="color"
                    >
                        Цвет:
                    </span>
                </div>
                <input 
                    class="model-field"
                    type="text" 
                    name="color" 
                    :disabled="actionType === 'view'" 
                    v-model="object.color"
                />
            </div>
        </template>
    </div>
    
</template>

<style lang='css'>
    span {
        margin-bottom: 0.5rem
    }
</style>

<script lang="ts">
    import { defineComponent, type PropType } from 'vue'

    import type { Select } from "@shared/types/interfaces"
    import * as validators from "@shared/types/validators"
    import { Scroll } from "@shared/ui/scroll"

    import type { UnitView } from "entities/unit/types/index"
    import { 
        BusLabels, 
        UnitColorLabels, 
        SelectBus, 
        SelectUnitColor 
    } from "entities/unit/schema"

    
    export default defineComponent({

        data(){
            console.log(`actionType: ${this.actionType}`)

            console.log(`object.bus: ${this.object.bus}, ${this.object.bus?.id}`)
            return {
                BusLabels, 
                UnitColorLabels, 
                SelectBus: SelectBus as Select, 
                SelectUnitColor: SelectUnitColor as Select
            }
        },

        components: {
            Scroll
        },

        props: {

            actionType: {
                type: String as PropType<string>,
                validator: validators.actionType
            },
            object: {
                type: Object as PropType<UnitView>,
                required: true
            },
        }
    })
    
</script>
