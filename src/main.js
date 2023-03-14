import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
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
import { faChevronLeft, faInfoCircle } from '@fortawesome/free-solid-svg-icons'

library.add(faChevronLeft)
library.add(faInfoCircle)
    // createApp(App).use(store).use(router).mount('#app')
const application = createApp(App)
application.use(store)
application.use(router)
application.use(VueAxios, axios)
application.component('font-awesome-icon', FontAwesomeIcon)
application.provide('axios', application.config.globalProperties.axios)
application.mount("#app")