<template>
	<h1 class="page-title">{{ page_title }}</h1>
	<div class="container">
		<form @submit.prevent="forgetPassword" class="form-box">
			<div class="form-group row mb-3">
				<div class="mx-auto col-sm-6 form-label">
					<label for="username">ชื่อผู้ใช้</label>
					<input type="text" class="form-control"
					id="username" v-model="username"
					placeholder="Enter Username"
					required
					/>
				</div>
			</div>
			<div class="form-group">
				<button class="btn btn-primary btn-block">ลืมรหัสผ่าน</button>
			</div>
		</form>
	</div>
</template>
<script>
import Swal from 'sweetalert2';
import helper from '@/helpers/helper';
import AuthService from '@/services/auth.service';

export default {
	name: 'forgetPasswordPage',
	data() {
		return {
			page_title: 'ลืมรหัสผ่าน',
			username: null
		}
	},
	methods: {
		async forgetPassword() {
			Swal.fire({
                title: "ยืนยัน?",
                text: "ต้องการรีเซ็ตรหัสผ่านหรือไม่?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "ยืนยัน",
                confirmButtonColor: "#039018",
                cancelButtonColor: '#d33',
                cancelButtonText: "ยกเลิก"
            }).then((result) => {
				if (result.isConfirmed) {
					helper.loadingAlert();
					AuthService.forgetPassword(this.username).then(
						(response) => {
							helper.successAlert(undefined, `ระบบได้ส่งรหัสผ่านใหม่ไปยังอีเมล<br/>${response}`, () => {
								this.$router.push("/login");
							});
						},
						(error) => {
							helper.failAlert(error);
						}
					)
				}
			})
		}
	}
}
</script>