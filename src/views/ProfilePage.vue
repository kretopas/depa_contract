<template>
    <h1 class="page-title">{{ page_title }}</h1>
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
                <form class="form-box">
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
            page_title: 'ข้อมูลผู้ใช้งาน',
            userDetail: '',
            name: '',
            company: '',
            email: '',
            editMode: false,
            imageWidth: '300px',
            file: null
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
            if (this.editMode == true) {
                this.editMode = false
            } else {
                this.editMode = true
            }
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
                    helper.loadingAlert();
                    var data = {
                        user_id: this.user,
                        name: this.name,
                        company: this.company,
                        email: this.email,
                    }
                    let formData = new FormData();
                    const json = JSON.stringify(data);
                    var fileCheck = 'withoutfile'
                    formData.append("user_data", json);
                    
                    if (this.file) {
                        formData.append("sign_img", this.file)
                        fileCheck = 'withfile'
                    }

                    UserService.updateUser(fileCheck, formData).then(
                        success => {
                            helper.successAlert(success, () => {
                                location.reload();
                            });
                        },
                        error => {
                            helper.failAlert(error);
                        }
                    )
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