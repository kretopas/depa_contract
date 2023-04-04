import api from "./api";

class UserService {
	getUserCurrent() {
		return api.get('/user/detail');
	}
}

export default new UserService()