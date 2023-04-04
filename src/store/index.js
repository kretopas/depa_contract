import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import { auth } from './auth.module'

export default createStore({
    state: {},
    getters: {
        accessToken: (state) => {
            return state.accessToken;
        },
    },
    mutations: {
        accessToken(state, accessToken) {
            state.user = accessToken;
        },
    },
    actions: {
        accessToken(context, accessToken) {
            context.commit('accessToken', accessToken);
        },
    },
    modules: {
        auth
    },
    plugins: [
        createPersistedState()
    ]
})