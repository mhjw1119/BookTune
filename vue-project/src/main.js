
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './index.css' // 또는 여러분이 만든 CSS 파일의 경로


const app = createApp(App)


app.use(createPinia())
app.use(router)

app.mount('#app')
