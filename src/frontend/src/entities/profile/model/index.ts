import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'

import store from '@shared/model/store'

import profile from 'entities/profile/model/store'
import leadStore from 'entities/lead/model/store'
import unitStore from 'entities/unit/model/store'


export default createStore({
    modules: {
        store,
        profile,
        leadStore,
        unitStore
    },
    plugins: [
        createPersistedState({
            paths: [
                'lead.lead',
                'profile.profile',
                'store.token',
                'store.refreshToken',
                'unit.unit'
            ]
        })
    ]
})