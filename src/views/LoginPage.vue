<template>
    <div class="container">
        <form @submit.prevent="handleSubmit">
            <div class="form-group">
                <label>ชื่อผู้ใช้</label>
                <input type="text" v-model="username" class="form-control" placeholder="Enter Username" />
            </div>
            <div class="form-group">
                <label>รหัสผ่าน</label>
                <input type="password" v-model="password" class="form-control" placeholder="Enter Password" />
            </div>
            <button class="btn btn-primary btn-block">Login</button>
        </form>
    </div>
</template>

<script>
import Swal from 'sweetalert2';

export default {
    name: 'loginPage',
    data() {
        return {
            username: '',
            password: '',
        }
    },
    methods: {
        async handleSubmit() {
            const data = {
                username: this.username,
                password: this.password
            };
            this.$store.dispatch('auth/login', data).then(
                () => {
                    this.$router.push("/")
                },
                (error) => {
                    console.log(error)
                    Swal.fire({
                        title: 'เกิดข้อผิดลพาด',
                        icon: 'warning',
                        html: 'ไม่สามารถเข้าสู่ระบบได้<br/>กรุณาตรวจสอบข้อมูลอีกครั้ง',
                        confirmButtonText: 'ตกลง'
                    })
                }
            )
        }
    }
}
</script>