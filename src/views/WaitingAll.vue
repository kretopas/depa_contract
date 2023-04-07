<template>
    <h1 class="page-title">{{ page_title }}</h1>
    <div class="container" v-if="currentUser && documents.length > 0">
        <div v-for="document in documents" v-bind:key="document">
            <div :class="'card text-bg-warning'">
                <div class="card-header">
                    <span>หมายเลขหนังสือ: <b>{{ document.name }}</b></span>
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
        <p style="margin: 10px;"><b>ไม่มีเอกสารที่รอการลงนามในขณะนี้</b></p>
    </div>
</template>

<script>
import DocumentService from '@/services/document.service';
import EventBus from '@/common/EventBus';

export default {
    name: 'WaitingTicket',
    data() {
        return {
            page_title: "เอกสารรอดำเนินการ",
            documents: []
        }
    },
    async mounted() {
        DocumentService.getWaitingDocuments().then(
            (response) => {
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
        //...mapGetters(['user']),
        //...mapGetters(['userGroup'])
        currentUser() {
            return this.$store.state.auth.user;
        }
    }
}
</script>

<style scoped>
.top-margin {
    margin-top: 15px;
}

.card {
    margin: 10px 15px 0px;
}

</style>
