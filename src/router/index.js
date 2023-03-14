import { createRouter, createWebHistory } from 'vue-router';
import store from '../store'
import WaitingAll from '../views/WaitingAll.vue';
import CompleteAll from '../views/CompleteAll.vue';
import SignPage from '../views/SignPage.vue';
import LoginPage from '../views/LoginPage.vue';
import ProfilePage from '../views/ProfilePage.vue';
import RegisterPage from '../views/RegisterPage.vue';

const routes = [{
        path: '/',
        name: 'waiting',
        component: WaitingAll,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/complete',
        name: 'complete',
        component: CompleteAll,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/sign/:id',
        name: 'sign',
        component: SignPage,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/profile',
        name: 'profile',
        component: ProfilePage,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/login',
        name: 'login',
        component: LoginPage
    },
    {
        path: '/register',
        name: 'register',
        component: RegisterPage
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!store.getters.isLoggedIn) {
            next({ name: 'login' })
        } else {
            next()
        }
    } else {
        next()
    }
})

export default router