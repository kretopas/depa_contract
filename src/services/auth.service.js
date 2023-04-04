import api from "./api";
import TokenService from "./token.service";

class AuthService {
	login(user) {
		return api.post(
			'/login', {
				username: user.username,
				password: user.password
			}
		).then(response => {
			if (response.data.access_token) {
				TokenService.setUser(response.data);
			}
			return response.data;
		});
	}

	logout() {
		TokenService.removeUser();
	}
}

export default new AuthService()