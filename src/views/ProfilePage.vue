import { mapGetters } from 'vuex';
<template>
    <div class="container">
        {{ user }}
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
    name: 'ProfilePage',
    data() {
        return {}
    },
    computed: {
        ...mapGetters(['user'])
    }
}
</script>