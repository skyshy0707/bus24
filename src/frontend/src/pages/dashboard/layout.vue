<template>
    <router-view/>

    <Wrapper>
        <sidebar>
        </sidebar>
    </Wrapper>
    

</template>

<script lang="ts">

import { defineComponent } from 'vue'

import { Wrapper } from "@shared/ui/themes"
import { sidebar } from "features/sidebar"

export default defineComponent({
    components: {
        sidebar,
        Wrapper
    }
})

</script>