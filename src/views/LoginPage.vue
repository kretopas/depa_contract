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
            this.axios({
                method: 'post',
                url: `${process.env.VUE_APP_API}/login`,
                data: data,
                headers: { "Content-Type": "application/json" }
            }).then((response) => {
                if (response.data.data != false) {
                    localStorage.setItem('userid', response.data.data);
                    if (response.data.group == 1) {
                        this.$store.dispatch('userGroup', 'employee')
                    } else if (response.data.group == 9) {
                        this.$store.dispatch('userGroup', 'contractor')
                    }
                    this.$store.dispatch('isLoggedIn', true);
                    this.$store.dispatch('user', response.data.data);
                    this.$router.push("/");
                } else {
                    Swal.fire({
                        title: 'ผิดพลาด',
                        icon: 'error',
                        html: 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง',
                        confirmButtonText: 'ตกลง'
                    })
                }
            }).catch(() => {
                Swal.fire({
                    title: 'เกิดข้อผิดพลาด',
                    icon: 'warning',
                    html: 'ไม่สามารถเข้าสู่ระบบได้<br/>กรุณาตรวจสอบข้อมูลอีกครั้ง',
                    confirmButtonText: 'ตกลง'
                })
            })
        }
    }
}
</script>