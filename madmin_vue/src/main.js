import { createApp } from 'vue'
import App from './App.vue'
import MFileUpload from '@/views/MFileUpload.vue'

import 'tailwindcss/base.css'
import './app.css'

const components = { MFileUpload }

const mount = (component, id, context) => {
  const app = createApp(component, {context})
  app.mount(id)
}

window.vueMount = (id) => {
  const context = JSON.parse(document.getElementById(`${id}_vue_context`).textContent)
  const component = components[context.vue_context.component]
  mount(component, '#' + id, context)
}

if (import.meta.env.DEV) {
  mount(App, '#app')
}
