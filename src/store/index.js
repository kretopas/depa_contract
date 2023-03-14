import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'

export default createStore({
    state: {},
    getters: {
        user: (state) => {
            return state.user;
        },
        isLoggedIn: (state) => {
            return state.isLoggedIn
        }
    },
    mutations: {
        user(state, user) {
            state.user = user;
        },
        isLoggedIn(state, isLoggedIn) {
            state.isLoggedIn = isLoggedIn;
        }
    },
    actions: {
        user(context, user) {
            context.commit('user', user);
        },
        isLoggedIn(context, isLoggedIn) {
            context.commit('isLoggedIn', isLoggedIn);
        }
    },
    modules: {},
    plugins: [
        createPersistedState()
    ]
})