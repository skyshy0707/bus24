<template>
    <router-view/>
    <sidebar>
    </sidebar>
</template>

<script lang="ts">

import { defineComponent } from 'vue'
import { sidebar } from "features/sidebar"

export default defineComponent({
    components: {
        sidebar
    }
})

</script>