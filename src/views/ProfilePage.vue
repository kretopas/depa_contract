<template>
    <div class="profile-bg">
        <div class="container" v-if="currentUser">
            <div class="row">
            <div v-if="userDetail" class="col-lg-9 col-md-11 col-sm-13 mx-auto">
                <div class="card">
                <div v-if="!editMode" class="btn-row">
                    <button type="button" class="btn btn-warning btn-block"
                    @click="toggleEditMode()"
                    >
                        <font-awesome-icon icon="fas fa-pencil" /> แก้ไขข้อมูล
                    </button>
                </div>
                <div v-if="editMode" class="btn-inline">
                    <button type="button" class="btn btn-success" style="float: left;"
                    @click="sendEditData()"
                    >
                        <font-awesome-icon icon="fas fa-floppy-disk" /> บันทึก
                    </button>
                    <button type="button" class="btn btn-outline-secondary" style="float: right;"
                    @click="toggleEditMode()"
                    >
                        ยกเลิก
                    </button>
                </div>
                <!--<div v-if="editMode">
                    <button type="button" class="btn btn-secondary btn-block"
                    @click="toggleEditMode()"
                    >
                        ยกเลิก
                    </button>
                </div>-->
                <div>
                    <form class="form-box">
                        <div class="form-group row mb-3">
                            <label for="name" class="col-sm-2 col-form-label label">ชื่อ-นามสกุล</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control"
                                id="name" v-model="name"
                                required :readonly="!editMode" :disabled="!editMode"/>
                            </div>
                        </div>
                        <div class="form-group row mb-3">
                            <label for="company" class="col-sm-2 col-form-label label">บริษัท</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control"
                                id="company" v-model="company"
                                required :readonly="!editMode" :disabled="!editMode"/>
                            </div>
                        </div>
                        <div class="form-group row mb-3">
                            <label for="email" class="col-sm-2 col-form-label label">อีเมล</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control"
                                id="email" v-model="email"
                                required :readonly="!editMode" :disabled="!editMode"/>
                            </div>
                        </div>
                        <div class="form-group row mb-3">
                            <label for="sign_img" class="col-sm-2 col-form-label label">ภาพลายเซ็น</label>
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
                        <div class="form-group row mb-3" v-if="editMode">
                            <label for="new_password" class="col-sm-2 col-form-label label">รหัสผ่านใหม่</label>
                            <div class="col-sm-10" id="new_password">
                                <input type="password" class="form-control"
                                id="new_password" v-model="new_password"/>
                            </div>
                        </div>
                        <div class="form-group row mb-3" v-if="editMode">
                            <label for="new_password_confirm" class="col-sm-2 col-form-label label">ยืนยันรหัสผ่านใหม่</label>
                            <div class="col-sm-10">
                                <input type="password" class="form-control"
                                id="new_password_confirm" v-model="new_password_confirm"/>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            </div>
        </div>
    </div>
    </div>
</template>

<script>
import Swal from 'sweetalert2';
import UserService from '@/services/user.service';
import EventBus from '@/common/EventBus';
import helper from '@/helpers/helper';

export default {
    name: 'ProfilePage',
    data() {
        return {
            userDetail: '',
            name: '',
            company: '',
            email: '',
            editMode: false,
            imageWidth: '300px',
            file: null,
            new_password: null,
            new_password_confirm: null,
            changePassword: null
        }
    },
    async mounted() {
        UserService.getUserCurrent().then(
            (response) => {
                this.userDetail = response.data;
                this.name = this.userDetail.name;
                this.company = this.userDetail.company;
                this.email = this.userDetail.email;
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
            this.editMode = !this.editMode;
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
                    var passwordValidated = true;
                    if (this.new_password) {
                        if (this.new_password === this.new_password_confirm) {
                            this.changePassword = true;
                        } else {
                            this.changePassword = false;
                            passwordValidated = false;
                        }
                    }
                    if (passwordValidated) {
                        helper.loadingAlert();
                        var data = {
                            user_id: this.user,
                            name: this.name,
                            company: this.company,
                            email: this.email,
                        };
                        let formData = new FormData();
                        const json = JSON.stringify(data);
                        var fileCheck = 'withoutfile';
                        formData.append("user_data", json);
                        
                        if (this.file) {
                            formData.append("sign_img", this.file);
                            fileCheck = 'withfile';
                        }
                        UserService.updateUser(fileCheck, formData).then(
                            success => {
                                if (this.changePassword) {
                                    UserService.changePassword(this.new_password).then(
                                    success => {
                                        helper.successAlert(undefined, success, () => {
                                            location.reload();
                                        });
                                    },
                                    error => {
                                        helper.failAlert(error);
                                    }
                                )
                                } else {
                                    helper.successAlert(undefined, success, () => {
                                        location.reload();
                                    });
                                }
                            },
                            error => {
                                helper.failAlert(error);
                            }
                        )
                    } else {
                        helper.failAlert('รหัสผ่านกับตัวยืนยันรหัสผ่านต้องตรงกัน');
                    }
                }
            })
        },
        selectedFile(event) {
            this.file = event[0];
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
.card {
    border: 1px solid rgba(0, 0, 0, 0.3);
    box-shadow: 5px 5px rgba(0, 0, 0, 0.1);
}
</style>