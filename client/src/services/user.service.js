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
				return Promise.resolve('ระบบจะพาท่านกลับไปยังหน้าเข้าสู่ระบบ');
			} else {
				return Promise.reject('ไม่สามารถลงทะเบียนผู้ใช้งานได้')
			}
		})
	}

	updateUser(fileCheck, formData) {
		return api.post(
			`/user/update/${fileCheck}`,
			formData,
			{ "Content-Type": "multipart/form-data" }
		).then(response => {
			if (response.data != false) {
				return Promise.resolve('แก้ไขข้อมูลผู้ใช้สำเร็จ')
			} else {
				return Promise.reject('ไม่สามารถแก้ไขข้อมูลผู้ใช้งานได้')
			}
		})
	}

	changePassword(newPassword) {
		return api.post(
			`/user/password`,
			{
				new_password: newPassword
			}
		).then(response => {
			if (response.data != false) {
				return Promise.resolve('แก้ไขข้อมูลผู้ใช้และรหัสผ่านสำเร็จ')
			} else {
				return Promise.reject('ไม่สามารถแก้ไขข้อมูลผู้ใช้และรหัสผ่านได้')
			}
		})
	}

	checkDuplicateUser(username) {
		return api.post(
			`/user/check`,
			{
				username: username
			}
		).then(response => {
			if (response.data != false) {
				return true
			} else {
				return false
			}
		})
	}

	revokeCertificate() {
		return api.get(
			`/user/certificate/revoke`
		).then(response => {
			if (response.data != false) {
				return Promise.resolve("เพิกถอนใบรับรองอิเล็กทรอนิกส์สำเร็จ")
			} else {
				return Promise.reject("ไม่สามารถเพิกถอนใบรับรองอิเล็กทรอนิกส์ได้")
			}
		})
	}

	renewCertificate() {
		return api.get(
			`/user/certificate/renew`
		).then(response => {
			if (response.data != false) {
				return Promise.resolve("ขอใบรับรองอิเล็กทรอนิกส์ใหม่สำเร็จ")
			} else {
				return Promise.reject("ไม่สามารถขอใบรับรองอิเล็กทรอนิกส์ใหม่ได้")
			}
		})
	}
}

export default new UserService()