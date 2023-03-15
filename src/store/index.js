import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'

export default createStore({
    state: {},
    getters: {
        user: (state) => {
            return state.user;
        },
        userGroup: (state) => {
            return state.userGroup;
        },
        isLoggedIn: (state) => {
            return state.isLoggedIn
        }
    },
    mutations: {
        user(state, user) {
            state.user = user;
        },
        userGroup(state, userGroup) {
            state.userGroup = userGroup;
        },
        isLoggedIn(state, isLoggedIn) {
            state.isLoggedIn = isLoggedIn;
        }
    },
    actions: {
        user(context, user) {
            context.commit('user', user);
        },
        userGroup(context, userGroup) {
            context.commit('userGroup', userGroup);
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