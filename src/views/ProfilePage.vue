import { mapGetters } from 'vuex';
<template>
    <div class="container-fluid" v-if="user">
        <div align="center" v-if="userDetail">
            <div v-if="!editMode">
                <button type="button" class="btn btn-warning btn-left"
                @click="toggleEditMode()"
                >
                    <font-awesome-icon icon="fas fa-pencil" /> แก้ไข
                </button>
            </div>
            <div v-if="editMode">
                <button type="button" class="btn btn-secondary btn-left"
                @click="toggleEditMode()"
                >
                    ยกเลิก
                </button>
                <button type="button" class="btn btn-info btn-left"
                @click="sendEditData()"
                >
                    <font-awesome-icon icon="fas fa-floppy-disk" /> บันทึก
                </button>
            </div>
            <table width="80%" class="table table-bordered table-hover">
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
                            <input type="text" :value="userDetail.fullname"
                            @change="saveEditInput('fullname', $event.target.value)"
                            :readonly="!editMode" :disabled="!editMode"
                            />
                        </td>
                    </tr>
                    <tr>
                        <td>บริษัท</td>
                        <td>
                            <input type="text" :value="userDetail.company"
                            @change="saveEditInput(key, $event.target.value)"
                            :readonly="!editMode" :disabled="!editMode"
                            />
                        </td>
                    </tr>
                    <tr>
                        <td>อีเมล</td>
                        <td>
                            <input type="text" :value="userDetail.email"
                            @change="saveEditInput(key, $event.target.value)"
                            :readonly="!editMode" :disabled="!editMode"
                            />
                        </td>
                    </tr>
                    <tr>
                        <td>CAD Password</td>
                        <td>
                            <textarea cols="50" rows="5" type="text" :value="userDetail.cad_password"
                            @change="saveEditInput(key, $event.target.value)"
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
            </table>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import Swal from 'sweetalert2';

export default {
    name: 'ProfilePage',
    data() {
        return {
            userDetail: '',
            fullname: '',
            company: '',
            email: '',
            cad_password: '',
            editMode: false,
            imageWidth: '300px',
            file: null
        }
    },
    created() {
        let url = `${process.env.VUE_APP_API}/${this.userGroup}/user/${this.user}`
        this.axios({
            method: 'get',
            url: url,
            headers: { "Content-Type": "application/json" }
        }).then((response) => {
            if (response.data.data != false) {
                this.userDetail = response.data.data
                this.fullname = this.userDetail.fullname;
                this.company = this.userDetail.company;
                this.email = this.userDetail.email;
                this.cad_password = this.userDetail.cad_password;
            }
        })
    },
    methods: {
        saveEditInput(field, value) {
            this[field] = value;
            console.log(this[field]);
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
                        fullname: this.fullname,
                        company: this.company,
                        email: this.email,
                        cad_password: this.cad_password,
                    }
                    let formData = new FormData();
                    const json = JSON.stringify(data);
                    var file_check = 'withoutfile'
                    console.log(this.file);
                    formData.append("user_data", json);
                    
                    if (this.file) {
                        formData.append("sign_img", this.file)
                        file_check = 'withfile'
                    }

                    this.axios({
                        method: 'post',
                        url: `${process.env.VUE_APP_API}/${this.userGroup}/edit/user/${file_check}`,
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
                    }).catch((response) => {
                        console.log(response);
                    })
                }
            })
        },
        selectedFile(event) {
            this.file = event[0]
        },
    },
    computed: {
        ...mapGetters(['user']),
        ...mapGetters(['userGroup'])
    }
}
</script>

<style scoped>


</style>