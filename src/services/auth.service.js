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
			return response.data;
		});
	}

	logout() {
		TokenService.removeUser();
	}

	forgetPassword(username) {
		return api.get(`/forget/${username}`)
		.then(response => {
			if (response.data) {
				return response.data;
			} else {
				return Promise.reject("ไม่พบชื่อผู้ใช้งานนี้ในระบบ");
			}
		});
	}

	getOTP(username) {
		return api.post(`/otp/generate`, {
			username: username
		}).then(response => {
			return response.data;
		})
	}

	verifyOTP(otp, username, password) {
		return api.post(`/otp/verify`, {
			token: otp,
			username: username,
			password: password
		}).then(response => {
			if (response.data.access_token) {
				TokenService.setUser(response.data);
				return Promise.resolve();
			} else {
				return Promise.reject();
			}
		})
	}
}

export default new AuthService()