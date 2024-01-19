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
                <div class="col-lg-10 col-md-10 col-sm-12 mx-auto">
                    <div class="card">
						<button class="btn btn-outline-secondary" @click="goToSignin" style="width: 120px;">
							<font-awesome-icon icon="fas fa-chevron-left" /> เข้าสู่ระบบ
						</button>
                        <form @submit.prevent="sendRegisterData" class="form-box">
                            <div class="form-group row label">
                                <label for="name" class="col-sm-2 col-form-label">ชื่อ-นามสกุล</label>
                                <div class="col-sm-3 has-validation">
                                    <select
                                    class="form-select"
                                    :class="{
                                        'is-invalid': !namePrefix,
                                        'is-valid': namePrefix
                                    }"
                                    v-model="namePrefix" id="namePrefix"
                                    required>
                                        <option :value="''" selected disabled hidden>คำนำหน้า</option>
                                        <option v-for="(option, index) in namePrefixOptions" :value="option" v-bind:key="index">
                                            {{ option }}
                                        </option>
                                    </select>
                                    <div id="validationNamePrefix" class="invalid-feedback">
                                        กรุณาเลือกคำนำหน้าชื่อ
                                    </div>
                                </div>
                                <div class="col-sm-7">
                                    <input type="text" class="form-control"
                                    :class="{'is-valid': (name.length > 0)}"
                                    id="name" v-model="name" required />
                                </div>
                            </div>
                            <div class="form-group row label">
                                <label for="company" class="col-sm-2 col-form-label">บริษัท</label>
                                <div class="col-sm-10">
                                    <input type="text" class="form-control"
                                    :class="{'is-valid': (company.length > 0)}"
                                    id="company" v-model="company" required />
                                </div>
                            </div>
                            <div class="form-group row label">
                                <label for="email" class="col-sm-2 col-form-label">อีเมล</label>
                                <div class="col-sm-10">
                                    <input type="text"
                                    class="form-control"
                                    :class="{
                                        'is-valid': validateEmail(email),
                                        'is-invalid': (email.length > 0 && !validateEmail(email))
                                    }"
                                    id="email" v-model="email" required />
                                </div>
                            </div>
                            <div class="form-group row label">
                                <label for="img_file" class="col-sm-2 col-form-label">ภาพลายเซ็น</label>
                                <div class="col-sm-10">
                                    <input type="file" class="form-control" 
                                    id="image" name="image"
                                    accept="image/*"
                                    :class="(file != null) ? 'is-valid' : 'is-invalid'"
                                    required
                                        @change="selectedFile($event.target.files)" />
                                </div>
                            </div>
                            <div class="form-group row label">
                                <label for="username" class="col-sm-2 col-form-label">ชื่อผู้ใช้</label>
                                <div class="col-sm-10 has-validation">
                                    <input type="text" class="form-control"
                                    id="username" v-model="username" required
                                    @keyup="checkDuplicateUser(username)"
                                    :class="{
                                        'is-valid': usernameAvailable,
                                        'is-invalid': (username.length > 0 && !usernameAvailable)
                                    }"
                                    />
                                    <div id="validationEmail" class="invalid-feedback">
                                        มีชื่อผู้ใช้นี้ในระบบแล้ว
                                    </div>
                                </div>
                            </div>
                            <div class="form-group row label">
                                <label for="email" class="col-sm-2 col-form-label">รหัสผ่าน</label>
                                <div class="col-sm-10">
                                    <input type="password" id="password" v-model="password"
                                    class="form-control"
                                    :class="password_matched ? 'is-valid' : 'is-invalid'"
                                    required
                                    @keyup="checkPasswordMatched" />
                                </div>
                            </div>
                            <div class="form-group row label">
                                <label for="email" class="col-sm-2 col-form-label">ยืนยันรหัสผ่าน</label>
                                <div class="col-sm-10 has-validation">
                                    <input type="password" id="confirm_password" v-model="confirm_password"
                                        class="form-control"
                                        :class="password_matched ? 'is-valid' : 'is-invalid'"
                                        required
                                        @keyup="checkPasswordMatched" />
                                    <div id="validationMatchedPassword" class="invalid-feedback">รหัสผ่านไม่ตรงกัน</div>
                                </div>
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
            namePrefix: '',
            name: '',
            company: '',
            email: '',
            file: null,
            username: '',
            password: '',
            confirm_password: '',
            password_matched: null,
            namePrefixOptions: [
                'นาย',
                'นาง',
                'นางสาว'
            ],
            usernameAvailable: null
        }
    },
    methods: {
        checkDuplicateUser(username) {
            UserService.checkDuplicateUser(username).then(
                (response) => {
                    this.usernameAvailable = response;
                }
            )
        },
        validateEmail(email) {
            var re = /\S+@\S+\.\S+/;
            return re.test(email);
        },
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
            if (this.validateEmail(this.email) && this.password_matched) {
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
            } else {
                helper.failAlert("กรุณากรอกข้อมูลให้ถูกต้อง");
            }
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
<style scoped>
@import url('@/assets/css/forms.css');
</style>