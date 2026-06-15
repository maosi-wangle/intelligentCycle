import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import Vant from 'vant'
import 'vant/lib/index.css'

import App from './App.vue'
import routes, { setupRouterGuard } from './router'

const app = createApp(App)
const pinia = createPinia()
const router = createRouter({
  history: createWebHistory(),
  routes
})

setupRouterGuard(router)

app.use(pinia)
app.use(router)
app.use(Vant)

app.mount('#app')