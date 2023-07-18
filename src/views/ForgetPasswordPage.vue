<template>
	<div class="wrapper">
		<div class="container">
			<div class="box">
				<div></div>
				<div></div>
				<div></div>
				<div></div>
				<div></div>
				<div></div>
				<div></div>
				<div></div>
				<div></div>
				<div></div>
			</div>
			<div class="row">
				<div class="col-lg-4 col-md-6 col-sm-8 mx-auto">
					<div class="card">
						<button class="btn btn-outline-secondary" @click="goToSignin" style="width: 120px;">
							<font-awesome-icon icon="fas fa-chevron-left" /> เข้าสู่ระบบ
						</button>
						<form @submit.prevent="forgetPassword" class="form-box">
							<div class="form-group row mb-3">
								<div class="mx-auto form-label">
									<label for="username">ชื่อผู้ใช้</label>
									<input type="text" class="form-control" id="username" v-model="username"
										placeholder="Enter Username" required />
								</div>
							</div>
							<div class="form-group">
								<button class="btn btn-primary btn-block">ลืมรหัสผ่าน</button>
							</div>
						</form>
					</div>
				</div>
			</div>
		</div>
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
			username: null
		}
	},
	methods: {
		async forgetPassword() {
			Swal.fire({
				title: "ยืนยัน?",
				text: "ต้องการส่งคำขอรีเซ็ตรหัสผ่านหรือไม่?",
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
		},
		goToSignin() {
			this.$router.push("/login");
		}
	}
}
</script>
<style scoped>
@import url('@/assets/css/forms.css');
</style>