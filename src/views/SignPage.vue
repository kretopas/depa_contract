<template>
    <h1 class="page-title">{{ page_title }}</h1>
    <div class="container" v-if="currentUser">
        <div v-if="document">
            <div class="btn-row">
                <router-link to="/">
                    <button type="button" class="btn btn-outline-primary">
                        <font-awesome-icon icon="fas fa-chevron-left" /> Back
                    </button>
                </router-link>
            </div>
            <div class="form-box">
                <form @submit.prevent="signDocument">
                    <div class="form-group row mb-3">
                        <label for="doc_number" class="col-sm-2 col-form-label">
                            เลขหนังสือ
                        </label>
                        <div class="col-sm-10">
                            <input type="text" class="form-control"
                            id="doc_number" :value="document.name"
                            :readonly="true"/>
                        </div>
                    </div>
                    <div class="form-group row mb-3">
                        <label for="subject" class="col-sm-2 col-form-label">
                            ชื่อหนังสือ
                        </label>
                        <div class="col-sm-10">
                            <textarea cols="50" rows="4" class="form-control"
                            id="subject" :value="document.subject"
                            :readonly="true"/>
                        </div>
                        <div style="padding-top: 10px;">
                            <button class="btn btn-clear btn-block btn-warning">
                                ตัวอย่างเอกสาร
                            </button>
                            <button class="btn btn-clear btn-block btn-success">
                                ลงนาม
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        <div align="center" v-else-if="document == false">
            <p class="false-text">
                <b>ท่านไม่มีสิทธิ์ในการเข้าถึงหนังสือฉบับนี้<br />หรือ<br />หนังสือฉบับนี้ไม่อยู่ในสถานะสำหรับลงนาม</b></p>
        </div>
    </div>
</template>

<script>
//import { mapGetters } from 'vuex';
import Swal from 'sweetalert2';
//import api from '@/services/api';
import DocumentService from '@/services/document.service';
import EventBus from '@/common/EventBus';

export default {
    name: 'SignPage',
    data() {
        return {
            page_title: 'ลงนามเอกสาร',
            document: null
        }
    },
    async mounted() {
        DocumentService.getDocumentDetail(this.$route.params.id).then(
            (response) => {
                this.document = response.data
            },
            error => {
                this.content =
                (error.response && error.response.data && error.response.data.message) ||
                error.message ||
                error.toString()

                if (error.response && error.response.status === 403) {
                    EventBus.dispatch("logout");
                }
            }
        )
    },
    methods: {
        //LoadingAlert() {
        //    Swal.fire({
        //        title: 'กรุณารอสักครู่',
        //        allowOutsideClick: false
        //    })
        //    Swal.showLoading()
        //},
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
                    this.$parent.LoadingAlert();

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
        //...mapGetters(['user']),
        //...mapGetters(['userGroup'])
        currentUser() {
            return this.$store.state.auth.user;
        }
    }
}
</script>