<template>
    <h1 class="page-title">{{ page_title }}</h1>
    <div class="container" v-if="currentUser && documents.length > 0">
        <div v-for="document in documents" v-bind:key="document">
            <div class="card text-bg-success">
                <div class="card-header">
                    <span>หมายเลขหนังสือ: <strong>{{ document.name }}</strong></span>
                </div>
                <div class="card-body">
                    <p class="card-text">เรื่อง: {{ document.subject }}</p>
                    <router-link :to="'/signed/' + document.id">
                        <a class="btn btn-primary btn-right">
                            <font-awesome-icon icon="fas fa-info-circle"/> รายละเอียด
                        </a>
                    </router-link> 
                </div>
            </div>
        </div>
    </div>
    <div class="container" v-else>
        <p><strong>ไม่มีเอกสารที่ลงนามแล้ว</strong></p>
    </div>
</template>

<script>
import EventBus from '@/common/EventBus';
import DocumentService from '@/services/document.service';

export default {
    name: 'CompleteDocument',
    data() {
        return {
            page_title: "เอกสารที่ลงนามแล้ว",
            documents: []
        }
    },
    async mounted() {
        DocumentService.getSignedDocuments().then(
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