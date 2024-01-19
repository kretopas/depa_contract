<template>
  <MainHeader/>
  <router-view/>
</template>

<script>
import MainHeader from '@/components/MainHeader.vue';
import EventBus from '@/common/EventBus';

export default {
  name: 'MainApp',
  components: {
    MainHeader,
  },
  data() {
    return {
    }
  },
  methods: {
    logOut() {
      this.$store.dispatch('auth/logout');
      this.$router.push('/login');
    },
  },
  mounted() {
    EventBus.on("logout", () => {
      this.logOut()
    });
  },
  beforeUnmount() {
    EventBus.remove("logout");
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

@import url('@/assets/css/forms.css');
@import url('@/assets/css/profile.css');
@import url('@/assets/css/app.css');
@import url('@/assets/css/pagination.css');

</style>
