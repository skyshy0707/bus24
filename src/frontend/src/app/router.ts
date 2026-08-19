import {
    createRouter,
    createWebHistory
} from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.VITE_BASE_URL),
    routes: [
        {
            path: '/',
            component: () => import('pages/dashboard/layout.vue'),
            children: [
                {
                    path: '',
                    name: 'dashboard',
                    component: () => import('pages/dashboard/index.vue')
                }
            ]
        },
        {
            path: '/profile',
            name: 'profile',
            component: () => import('pages/profile/ui/index.vue'),
        }
    ]
})

export default router