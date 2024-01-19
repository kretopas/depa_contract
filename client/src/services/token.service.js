class TokenService {
	getLocalAccessToken() {
		const user = JSON.parse(localStorage.getItem("user"));
		return user?.access_token;
	}

	getLocalRefreshToken() {
        const user = JSON.parse(localStorage.getItem("user"));
        return user?.refresh_token;
    }

	updateLocalAccesstoken(token) {
        let user = JSON.parse(localStorage.getItem("user"));
        user.access_token = token;
        localStorage.setItem("user", JSON.stringify(user));
    }
	
	getUser() {
		return JSON.parse(localStorage.getItem("user"));
	}

	setUser(user) {
        localStorage.setItem("user", JSON.stringify(user));
    }

	removeUser() {
		localStorage.removeItem("user");
	}
}

export default new TokenService()