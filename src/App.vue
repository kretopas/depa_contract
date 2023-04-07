<template>
  <MainHeader/>
  <router-view/>
  <!-- <MainFooter/> -->
</template>

<script>
import MainHeader from '@/components/MainHeader.vue';
// import MainFooter from '@/components/MainFooter.vue';
import EventBus from '@/common/EventBus';

export default {
  name: 'MainApp',
  components: {
    MainHeader,
    // MainFooter
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

nav {
  padding: 30px;
}

.button-clear {
  margin-bottom: 5px;
}

.false-text {
  color: red;
}

.btn-right {
  float: right;
  margin: 10px
}

/*.btn-left {
  margin: 10px;
}*/

.form-group {
  margin-left: 10px;
  margin-bottom: 10px;
}

.btn-row {
  display: flex;
  padding-top: 10px;
}

.btn-block {
  margin-right: 10px;
}

.form-box {
  margin-top: 20px;
}

.form-label {
  text-align: left;
}

.page-title {
  margin-top: 10px;
}
/* nav a {
  font-weight: bold;
  color: #2c3e50;
} */

/*nav a.router-link-exact-active {
  color: #42b983;
} */
</style>
