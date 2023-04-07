import api from "./api";
class UserService {
	getUserCurrent() {
		return api.get('/user/detail');
	}

	registerUser(formData) {
		return api.post(
			'/user/register',
			formData,
			{ "Content-Type": "multipart/form-data" }
		).then(response => {
			if (response.data != false) {
				return true;
			} else {
				return Promise.reject('ไม่สามารถลงทะเบียนผู้ใช้งานได้')
			}
		})
	}
}

export default new UserService()