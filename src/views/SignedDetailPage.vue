<template>
	<h1 class="page-title">{{ page_title }}</h1>
	<div class="container" v-if="currentUser">
		<div v-if="document">
			<div class="btn-row">
				<router-link to="/complete">
					<button type="button" class="btn btn-outline-primary">
						<font-awesome-icon icon="fas fa-chevron-left" /> Back
					</button>
				</router-link>
			</div>
			<div class="form-box">
				<form>
					<div class="form-group row mb-3">
						<label for="doc_number" class="col-sm-2 col-form-label">
							เลขหนังสือ
						</label>
						<div class="col-sm-10">
							<input type="text" class="form-control"
							id="doc_number" :value="document.name"
							:readonly="true" :disabled="true"/>
						</div>
					</div>
					<div class="form-group row mb-3">
						<label for="subject" class="col-sm-2 col-form-label">
							ชื่อหนังสือ
						</label>
						<div class="col-sm-10">
							<textarea cols="50" rows="4" class="form-control"
							id="subject" :value="document.subject"
							:readonly="true" :disabled="true"/>
						</div>
						<div style="padding-top: 10px;">
							<button type="button" class="btn btn-clear btn-block btn-warning"
							@click="previewDocument">
								ตัวอย่างเอกสาร
							</button>
						</div>
					</div>
				</form>
			</div>
		</div>
		<div align="center" v-else-if="document == false">
			<p class="false-text">
				<strong>ท่านไม่มีสิทธิ์ในการเข้าถึงหนังสือฉบับนี้</strong>
			</p>
		</div>
	</div>
</template>

<script>
import DocumentService from '@/services/document.service';
import EventBus from '@/common/EventBus';
import Swal from 'sweetalert2';
import helper from '@/helpers/helper';

export default {
	name: 'SignedDetailPage',
	data() {
		return {
			page_title: 'รายละเอียดเอกสาร',
			document: null,
			preview_src: null,
			preview_pdf: false,
		}
	},
	async mounted() {
		DocumentService.getSignedDocumentDetail(this.$route.params.id).then(
			response => {
				this.document = response.data;
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
		showModalPreview() {
			Swal.fire({
				html: `<embed src="${this.preview_src}" type="application/pdf" height="500px" width="100%"/>`,
				showCloseButton: true,
				showConfirmButton: false,
				width: '80%'
			});
		},
        previewDocument() {
            if (!this.preview_src) {
                helper.loadingAlert();
                DocumentService.previewDocument(this.$route.params.id).then(
                    response => {
                        if (response.data != false) {
                            this.preview_src = `data:application/pdf;base64,${response.data}`;
                            this.showModalPreview();
                        }
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
            } else {
                this.showModalPreview();
            }
        },
	},
	computed: {
		currentUser() {
			return this.$store.state.auth.user;
		}
	}
}
</script>