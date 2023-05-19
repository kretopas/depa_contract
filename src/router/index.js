import { createRouter, createWebHistory } from 'vue-router';
import WaitingAll from '../views/WaitingAll.vue';
import CompleteAll from '../views/CompleteAll.vue';
import SignPage from '../views/SignPage.vue';
import LoginPage from '../views/LoginPage.vue';
import ProfilePage from '../views/ProfilePage.vue';
import RegisterPage from '../views/RegisterPage.vue';
import ForgetPasswordPage from '../views/ForgetPasswordPage.vue';

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
        component: LoginPage,
        meta: {
            requiresGuest: true
        }
    },
    {
        path: '/register',
        name: 'register',
        component: RegisterPage,
        meta: {
            requiresGuest: true
        }
    },
    {
        path: '/forget',
        name: 'forgetPassword',
        component: ForgetPasswordPage,
        meta: {
            requiresGuest: true
        }
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    const requiresAuth = to.matched.some((x) => x.meta.requiresAuth);
    const requiresGuest = to.matched.some((x) => x.meta.requiresGuest);
    const currentUser = localStorage.getItem('user');

    if (requiresAuth && !currentUser) {
        next({ name: 'login' });
    } else if (requiresGuest && currentUser) {
        next({ name: 'waiting' });
    } else {
        next();
    }
})

export default router