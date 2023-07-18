import AuthService from '@/services/auth.service';

const user = JSON.parse(localStorage.getItem('user'));
const initialState = user ? { status: { loggedIn: true }, user } : { status: { loggedIn: false }, user: null };

export const auth = {
    namespaced: true,
    state: initialState,
    actions: {
        login({ commit }, user) {
            return AuthService.login(user).then(
                user => {
                    commit('loginSuccess', user);
                    return Promise.resolve(user);
                },
                error => {
                    commit('loginFailure');
                    return Promise.reject(error);
                }
            )
        },
        logout({ commit }) {
            AuthService.logout();
            commit('logout');
        },
        refreshToken({ commit }, accessToken) {
            commit('refreshToken', accessToken);
        },
        otp({ commit }, otpData) {
            return AuthService.verifyOTP(otpData).then(
                () => {
                    console.log('otp success');
                    commit('otpSuccess');
                    return Promise.resolve();
                },
                error => {
                    console.log('otp fail');
                    commit('loginFailure');
                    return Promise.reject(error);
                }
            )
        }
    },
    mutations: {
        loginSuccess(state, user) {
            state.status.loggedIn = true;
            state.user = user;
        },
        loginFailure(state) {
            state.status.loggedIn = false;
            state.status.otp = false;
            state.user = null;
        },
        logout(state) {
            state.status.loggedIn = false;
            state.status.otp = false;
            state.user = null;
        },
        otpSuccess(state) {
            state.status.otp = true;
        },
        refreshToken(state, accessToken) {
            state.status.loggedIn = true;
            state.status.otp = true;
            state.user = {...state.user, accessToken: accessToken };
        }
    }
}