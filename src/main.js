import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import setupInterceptors from '@/services/setupInterceptors'

// ? import BootStrap
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'

import VueAxios from 'vue-axios'
import axios from 'axios'

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'
/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
/* import specific icons */
import { faChevronLeft, faInfoCircle, faPencil, faFloppyDisk } from '@fortawesome/free-solid-svg-icons'

library.add(faChevronLeft)
library.add(faInfoCircle)
library.add(faPencil)
library.add(faFloppyDisk)

setupInterceptors(store);

const app = createApp(App)
app.use(store)
app.use(router)
app.use(VueAxios, axios)
app.component('font-awesome-icon', FontAwesomeIcon)
app.provide('axios', app.config.globalProperties.axios)
app.mount("#app")