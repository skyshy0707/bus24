<template>
    <header>
        Свободная рассылка заявок на обслуживание городских автобусных маршрутов

        <Credentials
            :logged="logged"
        >
        </Credentials>
    </header>
</template>

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
            const b = this.user.token

            console.log(`b: ${b}`)
            const logGed = Boolean(this.user.token)
            console.log(`logGed: ${logGed}`)
            return logGed
        }
    }
})
</script>