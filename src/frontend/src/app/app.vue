<template>
    <Header></Header>
    <main>
        <suspense>
            <RouterView></RouterView>
        </suspense>
    </main>
</template>

<style lang="css">

main{
    margin-top: 50px;
    min-height: calc(100vh - 50px);
}

input, textarea, h4 {
    border-radius: 6px;
    margin-left: 0.4em
}

.model-field {
    width: 256px;
    padding-left: 1rem
}
.scroll-content::-webkit-scrollbar{
    width: 6px;
}
.scroll-content::-webkit-scrollbar-track  {
    background-color: rgba(217, 241, 0, 0.342);
}
.scroll-content::-webkit-scrollbar-thumb {
    background-color:rgba(65, 2, 90, 0.692);
    border-radius: 2px;
    box-shadow: inset 1px 1px 2px #ddd
}

</style>

<script lang="ts">


import { defineComponent } from "vue"

import { ProfileStore } from "entities/profile/ui/Profile"
import { Header } from "features/header"


export default defineComponent({
    name: 'App',
    mixins: [
        ProfileStore as any
    ],
    components: {
        Header
    }
})
</script>