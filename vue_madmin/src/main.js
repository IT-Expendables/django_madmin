import { createApp } from 'vue'
import App from './App.vue'
import MFileUpload from '@/views/MFileUpload.vue'

import 'tailwindcss/base.css'
import './app.css'

const components = { MFileUpload, App }

window.vueMount = (context) => {
  const component = components[context.component]
  const app = createApp(component, { context })
  app.mount(`#${context.id}`)
}

if (import.meta.env.DEV && location.port == '5199') {
  window.vueMount({ component: 'App', id: 'app' })
}
