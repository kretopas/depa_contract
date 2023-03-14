<template>
    <div class="container">
        <br/>
        <table width="80%" class="table table-bordered table-hover">
            <thead class="table-dark">
                <tr>
                    <th scope="col">รายการ</th>
                    <th scope="col">ข้อมูล</th>
                </tr>
            </thead>
            <tbody align="left">
                <tr>
                    <td>CAD Password:</td>
                    <td><textarea id="cad_password" name="cad_password" rows="6" cols="75" @change="$event => saveCadPassword($event.target.value)"></textarea></td>
                </tr>
                <tr>
                    <td>Upload Image:</td>
                    <td><input type="file" id="image" name="image" @change="$event => selectedFile($event.target.files)"/></td>
                </tr>
            </tbody>
        </table>
        <div style="padding-top: 10px;">
            <button @click="$event => signDocument()" type="button" class="btn btn-clear btn-success">
                LONG NAM
            </button>
        </div>
    </div>
</template>

<script>
import Swal from 'sweetalert2';

export default {
    data() {
        return {
            cad_password: '',
            file: null
        }
    },
    mounted() {

    },
    methods: {
        saveCadPassword(event) {
            this.cad_password = event
        },
        selectedFile(event) {
            this.file = event[0]
        },
        signDocument() {
            let formData = new FormData();

            if (this.file) {
                formData.append('cadPassword', this.cad_password)
                formData.append('imageFile', this.file)
                
                this.axios({
                    method: 'post',
                    url: `${process.env.VUE_APP_API}/sign`,
                    data: formData,
                    headers: { "Content-Type": "multipart/form-data"},
                }).then((response) => {
                    if (String(response.data.data).toLowerCase() === 'true') {
                        Swal.fire({
                                    title: 'สำเร็จ!',
                                    html: 'ลงนามสำเร็จแล้ว',
                                    icon: 'success',
                                    confirmButtonText: 'OK'
                                }).then(() => {
                                    location.reload();
                                })
                    }
                }).catch((response) => {
                    console.log(response)
                })
            }
        }
    },
}
</script>