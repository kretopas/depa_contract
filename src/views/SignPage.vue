<template>
    <router-link to="/">
        <button type="button" class="btn btn-outline-primary">
            <font-awesome-icon icon="fas fa-chevron-left" /> Back
        </button>
    </router-link>
    <div class="container-fluid" v-if="user">
        <div align="center" v-if="document">
            <table width="80%" class="table table-bordered table-hover">
                <thead class="table-dark">
                    <tr>
                        <th scope="col">รายการ</th>
                        <th scope="col">ข้อมูล</th>
                    </tr>
                </thead>
                <tbody align="left">
                    <tr>
                        <td>เลขหนังสือ</td>
                        <td>{{ document.name }}</td>
                    </tr>
                    <tr>
                        <td>ชื่อหนังสือ</td>
                        <td>{{ document.subject }}</td>
                    </tr>
                </tbody>
                <div style="padding-top: 10px">
                    <button type="button" class="btn btn-clear btn-success" @click="signDocument">
                        ลงนาม
                    </button>
                </div>
            </table>
        </div>
        <div align="center" v-else-if="document == false">
            <p class="false-text">
                <b>ท่านไม่มีสิทธิ์ในการเข้าถึงหนังสือฉบับนี้<br />หรือ<br />หนังสือฉบับนี้ไม่อยู่ในสถานะสำหรับลงนาม</b></p>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import Swal from 'sweetalert2';

export default {
    name: 'SignPage',
    data() {
        return {
            document: null
        }
    },
    created() {
        let url = `${process.env.VUE_APP_API}/${this.userGroup}/doc/detail/${this.user}/${this.$route.params.id}`
        this.axios({
            method: 'get',
            url: url,
            headers: { "Content-Type": "application/json" }
        }).then((response) => {
            if (response.data.data != false) {
                this.document = response.data.data
            } else {
                this.document = false
            }
        })
    },
    methods: {
        LoadingAlert() {
            Swal.fire({
                title: 'กรุณารอสักครู่',
                allowOutsideClick: false
            })
            Swal.showLoading()
        },
        signDocument() {
            Swal.fire({
                title: "ยืนยัน?",
                text: "ยืนยันการลงนามหรือไม่?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "ยืนยัน",
                confirmButtonColor: "#1E91EC",
                cancelButtonColor: "#d33",
                cancelButtonText: "ยกเลิก"
            }).then((result) => {
                if (result.isConfirmed) {
                    this.LoadingAlert();

                    let url = `${process.env.VUE_APP_API}/${this.userGroup}/doc/sign/${this.user}/${this.$route.params.id}`
                    this.axios({
                        method: 'get',
                        url: url,
                        headers: { "Content-Type": "application/json" }
                    }).then((response) => {
                        if (response.data.data != false) {
                            Swal.fire({
                                title: 'สำเร็จ!',
                                html: 'ลงนามสำเร็จแล้ว',
                                icon: 'success',
                                confirmButtonText: 'OK'
                            }).then(() => {
                                this.$router.push("/");
                            })
                        } else {
                            Swal.fire({
                                title: 'ผิดพลาด',
                                html: 'มีข้อผิดพลาดในการลงนาม',
                                icon: 'error',
                                confirmButtonText: 'OK'
                            })
                        }
                    }).catch(() => {
                        Swal.fire({
                            title: 'ผิดพลาด',
                            html: 'มีข้อผิดพลาดในการลงนาม',
                            icon: 'error',
                            confirmButtonText: 'OK'
                        })
                    })
                }
            })
        }
    },
    computed: {
        ...mapGetters(['user']),
        ...mapGetters(['userGroup'])
    }
}
</script>