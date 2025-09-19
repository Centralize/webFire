// (C) 2025 by OPNLAB Development. All rights reserved.
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia' // Import createPinia
import App from './App.vue'

import StatusView from './views/StatusView.vue'
import RulesView from './views/RulesView.vue'
import SettingsView from './views/SettingsView.vue'

// Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'

// Bootstrap JS
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

import './assets/main.css' // Assuming you have a main.css for global styles

const routes = [
  { path: '/', redirect: '/status' }, // Redirect root to status page
  { path: '/status', component: StatusView },
  { path: '/rules', component: RulesView },
  { path: '/settings', component: SettingsView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
const pinia = createPinia() // Create Pinia instance

app.use(router)
app.use(pinia) // Use Pinia
app.mount('#app')
