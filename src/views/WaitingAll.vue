<template>
    <div class="container" v-if="currentUser && documents != null && documents.length > 0">
        <div class="grid">
            <div v-for="document in documents.slice(((page-1)*itemPerPage), (page*itemPerPage))" v-bind:key="document">
                <div class="card" v-on:click="changePage(document.id)">
                    <div class="card-details">
                        <p class="text-title">{{ document.name }}</p>
                        <p class="text-body">{{ document.subject }}</p>
                    </div>
                    <div class="btn btn-primary card-button">
                        <font-awesome-icon icon="fas fa-pen-to-square"/> ลงนาม
                    </div>
                </div>
            </div>
        </div>
        <div>
            <vue-awesome-paginate
                v-model="page"
                :total-items="documents.length"
                :items-per-page="itemPerPage"
                :max-pages-shown="3"
                :show-ending-buttons="true"
                :hide-prev-next-when-ends="true"
            >
                <template #first-page-button>
                    <span>{{ "<<" }}</span>
                </template>
                <template #last-page-button>
                    <span>{{ ">>" }}</span>
                </template>
            </vue-awesome-paginate>
        </div>
    </div>
    <div class="container" v-else-if="ddocuments != null && documents.length == 0" style="margin-top: 20px;">
        <p class="false-text"><strong class="">ไม่มีเอกสารที่รอการลงนามในขณะนี้</strong></p>
    </div>
    <div class="container" v-else style="margin-top: 20px;">
        <p><strong>กำลังดึงข้อมูลรายการเอกสารที่รอการลงนาม โปรดรอสักครู่...</strong></p>
    </div>
</template>
<script>
import DocumentService from '@/services/document.service';
import EventBus from '@/common/EventBus';

export default {
    name: 'WaitingDocument',
    data() {
        return {
            documents: null,
            page: 1,
            itemPerPage: 8,
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
    },
    methods: {
        changePage(documentId) {
            this.$router.push(`/sign/${documentId}`);
        }
    }
}
</script>
<style scoped>
.container {
    border-radius: 5px;
    border: 1px solid rgba(0, 0, 0, 0.3);
    box-shadow: 5px 5px rgba(0, 0, 0, 0.1);
    margin-top: 10px;
    margin-bottom: 10px;
}

.grid {
    display: grid;
    grid-template-columns: 25% 25% 25% 25%;
    grid-template-rows: 2;
    grid-gap: 10px;
}
@media screen and (max-width: 900px) {
    .grid {
    grid-template-columns: 50% 50%;
    grid-template-rows: 4;
    }
}

.card {
    width: 75%;
    min-width: 180px;
    height: 254px;
    border-radius: 20px;
    background: #ffd301;
    position: relative;
    padding: 1.8rem;
    border: 2px solid #ffb921;
    transition: 0.5s ease-out;
    overflow: visible;
    margin-bottom: 5px;
    margin-left: auto;
    margin-right: auto;
}

.card-details {
    color: black;
    height: 100%;
    gap: .5em;
    display: grid;
    place-content: center;
}

.card-button {
    transform: translate(-50%, 125%);
    width: 60%;
    border-radius: 1rem;
    border: none;
    background-color: #0047ac;
    color: #fff;
    font-size: 1rem;
    padding: .5rem 1rem;
    position: absolute;
    left: 50%;
    bottom: 0;
    opacity: 0;
    transition: 0.3s ease-out;
}

.text-body {
    color: rgb(134, 134, 134);
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    line-height: 150%;
}

.text-title {
    font-size: 1.2em;
    font-weight: bold;
}

.card:hover {
    border-color: #1497d4;
    box-shadow: 0 4px 18px 0 rgba(0, 0, 0, 0.25);
    cursor: pointer;
}

.card:hover .card-button {
    transform: translate(-50%, 50%);
    opacity: 1;
}
</style>