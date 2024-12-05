import { createApp } from 'vue'
import App from './app.vue'
import { toast } from './plugins/toast'

const app = createApp(App)
app.use(toast)
app.mount('#app') 