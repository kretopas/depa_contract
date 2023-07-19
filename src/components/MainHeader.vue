<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-depa">
        <div class="container-fluid">
            <router-link to="/">
                <a class="navbar-brand">depa Contract</a>
            </router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarToggler"
                aria-controls="navbarToggler" aria-expanded="false" aria-label="Toggle Navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarToggler">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="currentUser">
                    <li class="nav-item">
                        <router-link to="/">
                            <a class="nav-link" aria-current="page" 
                            :class="($route.path == '/' || getPath($route.path) == 'sign') ? 'active' : ''">
                                รอดำเนินการ
                            </a>
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/complete">
                            <a class="nav-link"
                            :class="($route.path == '/complete' || getPath($route.path) == 'signed') ? 'active' : ''">
                                ลงนามแล้ว
                            </a>
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/profile">
                            <a class="nav-link" :class="$route.path == '/profile' ? 'active' : ''">
                                ข้อมูลของฉัน
                            </a>
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="#">
                            <a href="javascript:void(0)" @click="logoutClick" class="nav-link">
                                ออกจากระบบ
                            </a>
                        </router-link>
                    </li>
                </ul>
                <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-else>
                    <li class="nav-item">
                        <router-link to="/login">
                            <a class="nav-link" :class="$route.path == '/login' ? 'active' : ''">
                                เข้าสู่ระบบ
                            </a>
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/forget">
                            <a class="nav-link" :class="$route.path == '/forget' ? 'active' : ''">
                                ลืมรหัสผ่าน
                            </a>
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/register">
                            <a class="nav-link" :class="$route.path == '/register' ? 'active' : ''">
                                ลงทะเบียน
                            </a>
                        </router-link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
//import { mapGetters } from 'vuex';
import Swal from 'sweetalert2';

export default {
    name: 'mainHeader',
    data() {
        return {}
    },
    methods: {
        logoutClick() {
            Swal.fire({
                text: "ออกจากระบบหรือไม่?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "ออกจากระบบ",
                confirmButtonColor: "#d33",
                cancelButtonText: "ยกเลิก"
            }).then((result) => {
                if (result.isConfirmed) {
                    this.$store.dispatch('auth/logout');
                    this.$router.push('/login');
                }
            })
        },
        getPath(fullPath) {
            const actionPath = fullPath.split("/")[1];
            return actionPath;
        }
    },
    computed: {
        currentUser() {
            return this.$store.state.auth.status.otp;
        }
    }
}
</script>

<style scoped>
.bg-depa {
    background-color: #0c2f53;
}

a.nav-link:hover {
    color: #ffc600;
}

.active {
    border: solid yellow 1px;
    border-radius: 13px;
    box-shadow: 1px 2px #ffc600;
}

a {
    color: whitesmoke;
    text-decoration: none;
}

#navbarToggler .active {
    color: #ffc600;
}
</style>