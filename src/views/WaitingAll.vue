<template>
    <div class="container" v-if="currentUser && documents.length > 0">
        <div v-for="document in documents" v-bind:key="document">
            <div class="card text-bg-warning">
                <div class="card-header">
                    <span>หมายเลขหนังสือ: <strong>{{ document.name }}</strong></span>
                </div>
                <div class="card-body">
                    <p class="card-text">เรื่อง: {{ document.subject }}</p>
                    <router-link :to="'/sign/' + document.id">
                        <a class="btn btn-primary btn-right">
                            <font-awesome-icon icon="fas fa-info-circle"/> รายละเอียด
                        </a>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
    <div class="container" v-else>
        <p><strong>ไม่มีเอกสารที่รอการลงนามในขณะนี้</strong></p>
    </div>
</template>
<script>
import DocumentService from '@/services/document.service';
import EventBus from '@/common/EventBus';

export default {
    name: 'WaitingDocument',
    data() {
        return {
            documents: []
        }
    },
    async mounted() {
        DocumentService.getWaitingDocuments().then(
            response => {
                this.documents = response.data;
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
    computed: {
        currentUser() {
            return this.$store.state.auth.user;
        }
    }
}
</script>