<template>
    <div class="container" v-if="currentUser">
        <div v-if="userDetail">
            <div v-if="!editMode" class="btn-row">
                <button type="button" class="btn btn-warning btn-block"
                @click="toggleEditMode()"
                >
                    <font-awesome-icon icon="fas fa-pencil" /> แก้ไขข้อมูล
                </button>
            </div>
            <div v-if="editMode" class="btn-row">
                <button type="button" class="btn btn-secondary btn-block"
                @click="toggleEditMode()"
                >
                    ยกเลิก
                </button>
                <button type="button" class="btn btn-success btn-block"
                @click="sendEditData()"
                >
                    <font-awesome-icon icon="fas fa-floppy-disk" /> บันทึก
                </button>
            </div>
            <div>
                <form style="margin-top: 20px;">
                    <div class="form-group row mb-3">
                        <label for="name" class="col-sm-2 col-form-label">ชื่อ-นามสกุล</label>
                        <div class="col-sm-10">
                            <input type="text" class="form-control"
                            id="name" v-model="name"
                            required :readonly="!editMode" :disabled="!editMode"/>
                        </div>
                    </div>
                    <div class="form-group row mb-3">
                        <label for="company" class="col-sm-2 col-form-label">บริษัท</label>
                        <div class="col-sm-10">
                            <input type="text" class="form-control"
                            id="company" v-model="company"
                            required :readonly="!editMode" :disabled="!editMode"/>
                        </div>
                    </div>
                    <div class="form-group row mb-3">
                        <label for="email" class="col-sm-2 col-form-label">อีเมล</label>
                        <div class="col-sm-10">
                            <input type="text" class="form-control"
                            id="email" v-model="email"
                            required :readonly="!editMode" :disabled="!editMode"/>
                        </div>
                    </div>
                    <div class="form-group row mb-3">
                        <label for="cad_password" class="col-sm-2 col-form-label">CAD password</label>
                        <div class="col-sm-10">
                            <textarea cols="50" rows="4" class="form-control"
                            id="cad_password" v-model="cad_password"
                            required :readonly="!editMode" :disabled="!editMode"/>
                        </div>
                    </div>
                    <div class="form-group row mb-3">
                        <label for="sign_img" class="col-sm-2 col-form-label">ภาพลายเซ็น</label>
                        <div class="col-sm-10" id="sign_img">
                            <div v-if="editMode">
                                <input type="file" class="form-control"
                                id="image" name="image"
                                @change="$event => selectedFile($event.target.files)"/>
                            </div>
                            <img v-bind:src="'data:image/png;base64,'+userDetail.sign_img"
                            style="width: 200px; height: 100px;"
                            />
                        </div>
                    </div>
                </form>
            </div>
            <!--<table width="80%" class="table table-bordered table-hover">
                <thead class="table-dark">
                    <tr>
                        <th scope="col">รายการ</th>
                        <th scope="col">ข้อมูล</th>
                    </tr>
                </thead>
                <tbody align="left">
                    <tr>
                        <td>ชื่อ-นามสกุล</td>
                        <td>
                            <input type="text" :value="userDetail.name"
                            @change="saveEditInput('name', $event.target.value)"
                            :readonly="!editMode" :disabled="!editMode"
                            />
                        </td>
                    </tr>
                    <tr>
                        <td>บริษัท</td>
                        <td>
                            <input type="text" :value="userDetail.company"
                            @change="saveEditInput('company', $event.target.value)"
                            :readonly="!editMode" :disabled="!editMode"
                            />
                        </td>
                    </tr>
                    <tr>
                        <td>อีเมล</td>
                        <td>
                            <input type="text" :value="userDetail.email"
                            @change="saveEditInput('email', $event.target.value)"
                            :readonly="!editMode" :disabled="!editMode"
                            />
                        </td>
                    </tr>
                    <tr>
                        <td>CAD Password</td>
                        <td>
                            <textarea cols="50" rows="5" type="text" :value="userDetail.cad_password"
                            @change="saveEditInput('cad_password', $event.target.value)"
                            :readonly="!editMode" :disabled="!editMode"
                            />
                        </td>
                    </tr>
                    <tr>
                        <td>ภาพลายเซ็น</td>
                        <td>
                            <img v-bind:src="'data:image/png;base64,'+userDetail.sign_img"
                            style="width: 200px; height: 100px;"
                            />
                            <div v-if="editMode">
                                <input type="file" id="image" name="image" @change="$event => selectedFile($event.target.files)"/>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>-->
        </div>
    </div>
</template>

<script>
import Swal from 'sweetalert2';
import api from '@/services/api';
import UserService from '@/services/user.service';
import EventBus from '@/common/EventBus';

export default {
    name: 'ProfilePage',
    data() {
        return {
            userDetail: '',
            name: '',
            company: '',
            email: '',
            cad_password: '',
            editMode: false,
            imageWidth: '300px',
            file: null
        }
    },
    async mounted() {
        UserService.getUserCurrent().then(
            (response) => {
                this.userDetail = response.data;
                // สำหรับส่งข้อมูลไปแก้ไขข้อมูลผู้ใช้
                this.name = this.userDetail.name;
                this.company = this.userDetail.company;
                this.email = this.userDetail.email;
                this.cad_password = this.userDetail.cad_password;
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
        saveEditInput(field, value) {
            this[field] = value;
        },
        toggleEditMode() {
            if (this.editMode == true) {
                this.editMode = false
            } else {
                this.editMode = true
            }
        },
        LoadingAlert() {
            Swal.fire({
                title: 'กรุณารอสักครู่',
                allowOutsideClick: false
            })
            Swal.showLoading()
        },
        sendEditData() {
            Swal.fire({
                title: "ยืนยัน?",
                text: "เปลี่ยนข้อมูลผู้ใช้หรือไม่?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "ยืนยัน",
                confirmButtonColor: "#039018",
                cancelButtonColor: '#d33',
                cancelButtonText: "ยกเลิก"
            }).then((result) => {
                if (result.isConfirmed) {
                    this.LoadingAlert();
                    var data = {
                        user_id: this.user,
                        name: this.name,
                        company: this.company,
                        email: this.email,
                        cad_password: this.cad_password,
                    }
                    let formData = new FormData();
                    const json = JSON.stringify(data);
                    var file_check = 'withoutfile'
                    formData.append("user_data", json);
                    
                    if (this.file) {
                        formData.append("sign_img", this.file)
                        file_check = 'withfile'
                    }

                    api({
                        method: 'post',
                        url: `/user/update/${file_check}`,
                        data: formData,
                        headers: { "Content-Type": "multipart/form-data"},
                    }).then((response) => {
                        if (response.data.data != false) {
                            Swal.fire({
                                        title: 'สำเร็จ!',
                                        html: 'เปลี่ยนข้อมูลผู้ใช้สำเร็จแล้ว',
                                        icon: 'success',
                                        confirmButtonText: 'OK'
                                    }).then(() => {
                                        location.reload();
                                    })
                        } else {
                            Swal.fire({
                                title: 'ผิดพลาด',
                                html: 'มีข้อผิดพลาดในการเปลี่ยนข้อมูลผู้ใช้',
                                icon: 'error',
                                confirmButtonText: 'OK'
                            })
                        }
                    }).catch(() => {
                        Swal.fire({
                            title: 'ผิดพลาด',
                            html: 'มีช้อผิดพลาดในการลงนาม',
                            icon: 'error',
                            confirmButtonText: 'OK'
                        })
                    })
                }
            })
        },
        selectedFile(event) {
            this.file = event[0]
        },
    },
    computed: {
        currentUser() {
            return this.$store.state.auth.user;
        }
    }
}
</script>

<style scoped>
</style>