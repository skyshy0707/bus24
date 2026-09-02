<template>
    <header>
        Свободная рассылка заявок на обслуживание городских автобусных маршрутов

        <Credentials
            :logged="logged"
        >
        </Credentials>
    </header>
</template>

<style lang="css">

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