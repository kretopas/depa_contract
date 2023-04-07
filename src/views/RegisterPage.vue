<template>
    <h1 class="page-title">{{ page_title }}</h1>
    <div class="container">
        <form @submit.prevent="sendRegisterData" class="form-box">
            <div class="form-group row">
                <label for="name" class="col-sm-2 col-form-label">ชื่อ-นามสกุล</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" 
                    id="name" v-model="name"
                    required/>
                </div>
            </div>
            <div class="form-group row">
                <label for="company" class="col-sm-2 col-form-label">บริษัท</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" 
                    id="company" v-model="company"
                    required/>
                </div>
            </div>
            <div class="form-group row">
                <label for="email" class="col-sm-2 col-form-label">อีเมล</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" 
                    id="email" v-model="email"
                    required/>
                </div>
            </div>
            <!--<div class="form-group row">
                <label for="cad_password" class="col-sm-2 col-form-label">CAD Password</label>
                <div class="col-sm-10">
                    <textarea cols="50" rows="5" class="form-control"
                    type="text" v-model="cad_password"
                    required/>
                </div>
            </div>-->
            <div class="form-group row">
                <label for="img_file" class="col-sm-2 col-form-label">ภาพลายเซ็น</label>
                <div class="col-sm-10">
                    <input type="file" class="form-control"
                    id="image" name="image"
                    required
                    @change="selectedFile($event.target.files)"/>
                </div>
            </div>
            <div class="form-group row">
                <label for="username" class="col-sm-2 col-form-label">ชื่อผู้ใช้</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" 
                    id="username" v-model="username"
                    required/>
                </div>
            </div>
            <div class="form-group row">
                <label for="email" class="col-sm-2 col-form-label">รหัสผ่าน</label>
                <div class="col-sm-10">
                    <input type="password" id="password"
                    v-model="password" class="form-control"
                    required
                    @keyup="checkPasswordMatched"/>
                </div>
            </div>
            <div class="form-group row">
                <label for="email" class="col-sm-2 col-form-label">ยืนยันรหัสผ่าน</label>
                <div class="col-sm-10">
                    <input type="password" id="confirm_password"
                    v-model="confirm_password" class="form-control"
                    required
                    @keyup="checkPasswordMatched"/>
                </div>
                <p class="false-text" v-if="password_matched == false">รหัสผ่านไม่ตรงกัน</p>
            </div>
            <button class="btn btn-primary btn-block">Register</button>
        </form>
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
            page_title: 'ลงทะเบียนผู้ใช้งาน',
            name: '',
            company: '',
            email: '',
            //cad_password: '',
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
                        //cad_password: this.cad_password,
                        username: this.username,
                        password: this.password
                    }
                    let formData = new FormData();
                    const json = JSON.stringify(data);
                    formData.append("user_data", json);
                    formData.append("sign_img", this.file);
                    UserService.registerUser(formData).then(
                        () => {
                            Swal.fire({
                                title: 'ลงทะเบียนสำเร็จ',
                                html: 'ระบบจะพาท่านกลับไปยังหน้าเข้าสู่ระบบ',
                                icon: 'success',
                                confirmButtonText: 'ตกลง'
                            }).then(() => {
                                this.$router.push("/");
                            })
                        },
                        (err) => {
                            Swal.fire({
                                title: 'ผิดพลาด',
                                icon: 'error',
                                html: err,
                                confirmButtonText: 'ตกลง'
                            })
                        }
                    )
                    //this.axios({
                    //    method: 'post',
                    //    url: `${process.env.VUE_APP_API}/contractor/register/user`,
                    //    data: formData,
                    //    headers: { "Content-Type": "multipart/form-data" },
                    //}).then((response) => {
                    //    if (response.data.data != false) {
                    //        Swal.fire({
                    //            title: 'ลงทะเบียนสำเร็จ',
                    //            html: 'ระบบจะพาท่านกลับไปยังหน้าเข้าสู่ระบบ',
                    //            icon: 'success',
                    //            confirmButtonText: 'ตกลง'
                    //        }).then(() => {
                    //            this.$router.push("/");
                    //        })
                    //    } else {
                    //        Swal.fire({
                    //            title: 'ผิดพลาด',
                    //            icon: 'error',
                    //            html: 'ไม่สามารถลงทะเบียนผู้ใช้งานได้',
                    //            confirmButtonText: 'ตกลง'
                    //        })
                    //    }
                    //})
                }
            })
        },
        selectedFile(event) {
            this.file = event[0]            
        }
    },
}
</script>