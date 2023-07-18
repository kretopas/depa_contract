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
                <div class="col-lg-9 col-md-10 col-sm-12 mx-auto">
                    <div class="card">
						<button class="btn btn-outline-secondary" @click="goToSignin" style="width: 120px;">
							<font-awesome-icon icon="fas fa-chevron-left" /> เข้าสู่ระบบ
						</button>
                        <form @submit.prevent="sendRegisterData" class="form-box">
                            <div class="form-group row label">
                                <label for="name" class="col-sm-2 col-form-label">ชื่อ-นามสกุล</label>
                                <div class="col-sm-10">
                                    <input type="text" class="form-control" id="name" v-model="name" required />
                                </div>
                            </div>
                            <div class="form-group row label">
                                <label for="company" class="col-sm-2 col-form-label">บริษัท</label>
                                <div class="col-sm-10">
                                    <input type="text" class="form-control" id="company" v-model="company" required />
                                </div>
                            </div>
                            <div class="form-group row label">
                                <label for="email" class="col-sm-2 col-form-label">อีเมล</label>
                                <div class="col-sm-10">
                                    <input type="text" class="form-control" id="email" v-model="email" required />
                                </div>
                            </div>
                            <div class="form-group row label">
                                <label for="img_file" class="col-sm-2 col-form-label">ภาพลายเซ็น</label>
                                <div class="col-sm-10">
                                    <input type="file" class="form-control" id="image" name="image" required
                                        @change="selectedFile($event.target.files)" />
                                </div>
                            </div>
                            <div class="form-group row label">
                                <label for="username" class="col-sm-2 col-form-label">ชื่อผู้ใช้</label>
                                <div class="col-sm-10">
                                    <input type="text" class="form-control" id="username" v-model="username" required />
                                </div>
                            </div>
                            <div class="form-group row label">
                                <label for="email" class="col-sm-2 col-form-label">รหัสผ่าน</label>
                                <div class="col-sm-10">
                                    <input type="password" id="password" v-model="password" class="form-control" required
                                        @keyup="checkPasswordMatched" />
                                </div>
                            </div>
                            <div class="form-group row label">
                                <label for="email" class="col-sm-2 col-form-label">ยืนยันรหัสผ่าน</label>
                                <div class="col-sm-10">
                                    <input type="password" id="confirm_password" v-model="confirm_password"
                                        class="form-control" required @keyup="checkPasswordMatched" />
                                </div>
                                <p class="false-text" v-if="password_matched == false">รหัสผ่านไม่ตรงกัน</p>
                            </div>
                            <button class="btn btn-primary btn-block">สมัครสมาชิก</button>
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
import UserService from '@/services/user.service';

export default {
    name: 'RegisterPage',
    data() {
        return {
            name: '',
            company: '',
            email: '',
            file: null,
            username: '',
            password: '',
            confirm_password: '',
            password_matched: null,
        }
    },
    methods: {
        checkPasswordMatched() {
            if (this.password.length > 0 && this.confirm_password.length > 0) {
                if (this.password === this.confirm_password) {
                    this.password_matched = true
                } else {
                    this.password_matched = false
                }
            } else {
                this.password_matched = null
            }
        },
        sendRegisterData() {
            Swal.fire({
                title: "ลงทะเบียน?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "ยืนยัน",
                confirmButtonColor: "#039018",
                cancelButtonText: "ยกเลิก",
                cancelButtonColor: "#d33"
            }).then((result) => {
                if (result.isConfirmed) {
                    helper.loadingAlert();
                    var data = {
                        name: this.name,
                        company: this.company,
                        email: this.email,
                        username: this.username,
                        password: this.password
                    }
                    let formData = new FormData();
                    const json = JSON.stringify(data);
                    formData.append("user_data", json);
                    formData.append("sign_img", this.file);
                    UserService.registerUser(formData).then(
                        success => {
                            helper.successAlert(undefined, success, () => {
                                this.$router.push("/");
                            })
                        },
                        error => {
                            helper.failAlert(error);
                        }
                    )
                }
            })
        },
        selectedFile(event) {
            this.file = event[0]
        },
		goToSignin() {
			this.$router.push("/login");
		}
    },
}
</script>