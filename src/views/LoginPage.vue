<template>
    <h1 class="page-title">{{ page_title }}</h1>
    <div class="container">
        <div class="form-box">
            <form @submit.prevent="handleSubmit">
                <div class="form-group row mb-3">
                    <div class="mx-auto col-sm-4 form-label">
                        <label for="username">ชื่อผู้ใช้</label>
                        <input type="text" class="form-control" 
                        id="username" v-model="username"
                        placeholder="Enter Username"
                        required
                        />
                    </div>
                </div>
                <div class="form-group row mb-3">
                    <div class="mx-auto col-sm-4 form-label">
                        <label for="password">รหัสผ่าน</label>
                        <input type="password" class="form-control"
                        id="password" v-model="password"
                        placeholder="Enter Password"
                        required
                        />
                    </div>
                </div>
                <div class="form-group row mb-3">
                    <div class="mx-auto col-sm-4 form-label">
                        <p class="false-text" v-if="validate == false">ชื่อผู้ใช้/รหัสผ่านไม่ถูกต้อง</p>
                        <button class="btn btn-primary btn-block">เข้าสู่ระบบ</button>
                        <button type="button" class="btn btn-primary btn-block" @click="goRegister">ลงทะเบียน</button>
                    </div>
                </div>
                <div class="form-group row mb-3">
                    <div class="mx-auto col-sm-4 form-label">
                        <router-link to="/forget">
                            ลืมรหัสผ่าน
                        </router-link>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import Swal from 'sweetalert2';

export default {
    name: 'loginPage',
    data() {
        return {
            page_title: 'เข้าสู่ระบบ',
            username: null,
            password: null,
            validate: null,
        }
    },
    methods: {
        async handleSubmit() {
            const data = {
                username: this.username,
                password: this.password
            };
            this.$store.dispatch('auth/login', data).then(
                (response) => {
                    if (response) {
                        this.validate = true;
                        this.$router.push("/")
                    } else {
                        this.validate = false;
                    }
                },
                () => {
                    Swal.fire({
                        title: 'เกิดข้อผิดลพาด',
                        icon: 'warning',
                        html: 'ไม่สามารถเข้าสู่ระบบได้<br/>กรุณาตรวจสอบข้อมูลอีกครั้ง',
                        confirmButtonText: 'ตกลง'
                    })
                }
            )
        },
        goRegister() {
            this.$router.push("/register")
        }
    }
}
</script>