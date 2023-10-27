import axiosInstance from './api';
import TokenService from './token.service';
import router from '@/router';

const exceptions = ['/login', 'register', 'forget'];

const setup = (store) => {
    axiosInstance.interceptors.request.use(
        (config) => {
            const token = TokenService.getLocalAccessToken();
            if (token) {
                config.headers["Authorization"] = 'Bearer ' + token;
            }
            return config;
        },
        (error) => {
            return Promise.reject(error);
        }
    )
    axiosInstance.interceptors.response.use(
        (res) => {
            return res;
        },
        async(err) => {
            const originalConfig = err.config;
            if (!exceptions.includes(originalConfig.url) && err.response) {
                if (err.response.status === 403 && !originalConfig._retry) {
                    originalConfig._retry = true;
                    try {
                        const rs = await axiosInstance.post("/refresh", {
                            token: TokenService.getLocalRefreshToken(),
                        });
                        const { access_token } = rs.data;
                        store.dispatch('auth/refreshToken', access_token);
                        TokenService.updateLocalAccesstoken(access_token);
                        return axiosInstance(originalConfig);
                    } catch (_error) {
                        TokenService.removeUser();
                        router.push('/login');
                    }
                }
            }
            return Promise.reject(err);
        }
    );
};

export default setup;