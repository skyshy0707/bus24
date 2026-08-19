<template>
    <div>
        <div>
            
            <iframe 
                v-if="actionType != 'create'"
                :src="object.route_wiki_url"
                width="100%"
                allowfullscreen="true"
                style="aspect-ratio: 16/9"
            >
            </iframe>
        </div>
        <div>
            <div
                class="model-field"
            >
                <span 
                    for="route_no" 
                >
                    № маршрута:
                </span>
            </div>
            <input 
                class="model-field"
                type="text" 
                name="route_no" 
                :disabled="actionType === 'view'" 
                v-model="object.route_no"
                required
            />
        </div>
        <div>
            <div
                class="model-field"
            >
                <span 
                    for="route_wiki_url" 
                >
                    Url маршрута:
                </span>
            </div>
            <input 
                class="model-field"
                type="url" 
                name="route_wiki_url" 
                :disabled="actionType === 'view'" 
                v-model="object.route_wiki_url"
                required
            />
        </div>
        <div>
            <div
                class="model-field"
            >
                <span 
                    for="capacity_class"
                >
                    Класс вместимости:
                </span>
            </div>
            <Scroll
                v-if="actionType == 'edit' || actionType == 'create'"
                :endpoint="'buses/cathegory'"
                :labels="BusCathegoryLabels"
                :select="SelectBusCathegory"
                :object="object"
                v-model="object.capacity_class"
            >

            </Scroll>
            <input 
                class="model-field"
                v-if="actionType=='view'"
                type="string" 
                name="capacity_class" 
                :disabled="true" 
                v-model="object.capacity_class"
                required
            />
        </div>
        <div>
            <div
                class="model-field"
            >
                <span 
                    for="units_per_route"
                >
                    Количество машин:
                </span>
            </div>
            <input 
                class="model-field"
                type="number" 
                name="units_per_route" 
                :disabled="actionType === 'view'"
                v-model="object.units_per_route"
                required
            />
        </div>
        <span 
            v-if="actionType === 'edit' || actionType === 'view'" 
        >
            Изменён: {{ parseDate(object.date) }}
        </span>
    </div>
</template>

<script lang="ts">
    import { defineComponent, type PropType } from 'vue'

    import { parseDate } from "@shared/lib/format"
    import type { Select } from "@shared/types/interfaces"
    import * as validators from "@shared/types/validators"
    import { Scroll } from "@shared/ui/scroll"

    import type { LeadView } from "entities/lead/types/index"
    import { 
        BusCathegoryLabels,
        SelectBusCathegory
    } from "entities/lead/schema"
    

    export default defineComponent({

        components: {
            Scroll
        },

        data() {
            return {
                parseDate,
                BusCathegoryLabels,
                SelectBusCathegory: SelectBusCathegory as Select
            }
        },
        props: {

            actionType: {
                type: String as PropType<string>,
                validator: validators.actionType
            },
            object: {
                type: Object as PropType<LeadView>,
                required: true
            },
        }
    })
    
</script>
