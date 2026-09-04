<template>
    <header>
        <p
            class="h-description"
        >
        Свободная рассылка заявок на обслуживание городских автобусных маршрутов
        </p>

        <Credentials
            :logged="logged"
        >
        </Credentials>
    </header>
</template>

<style lang="css">
.h-description{
    font: Franklin Gothic Small;
    margin-left: 0.5em;
    margin-top: 0.1em 
}
</style>

<script lang="ts">

import { defineComponent } from 'vue'

import { ProfileStore } from "entities/profile/ui/Profile"


import { Credentials } from "features/credentials"


export default defineComponent({
    components: {
        Credentials
    },
    mixins: [ 
        ProfileStore as any,

    ],
    computed: {
        logged() {
            return Boolean(this.user.token)
        }
    }
})
</script>