<template>
    <div class="container" v-if="user">
        <div v-for="document in documents" v-bind:key="document">
            <div :class="'card text-bg-warning'">
                <div class="card-header">
                    <span>หมายเลขหนังสือ: <b>{{ document.name }}</b></span>
                </div>
                <div class="card-body">
                    <p class="card-text">เรื่อง: {{ document.subject }}</p>
                    <router-link :to="'/sign/' + document.id">
                        <a class="btn btn-primary btn-right">
                            <font-awesome-icon icon="fas fa-info-circle" /> รายละเอียด
                        </a>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
    name: 'WaitingTicket',
    data() {
        return {
            documents: []
        }
    },
    created() {
        let url = `${process.env.VUE_APP_API}/doc/waiting/${this.user}`
        this.axios({
            method: 'get',
            url: url,
            headers: { "Content-Type": "application/json" }
        }).then((response) => {
            if (response.data.data != false) {
                this.documents = response.data.data
            }
        })
    },
    computed: {
        ...mapGetters(['user'])
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
