// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './src/plugins/vuetify'
import 'chart.js'

const app = createApp(App)

app.use(router)
app.use(store)
app.use(vuetify)

app.mount('#app')