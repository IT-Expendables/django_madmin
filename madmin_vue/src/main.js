import { createApp } from 'vue'
import App from './App.vue'
import { updateContext } from '@/managers/context'
import MFileUpload from '@/views/MFileUpload.vue'

import 'tailwindcss/base.css'
import './app.css'

const components = { MFileUpload }

const mount = (component, id) => {
  const app = createApp(component)
  app.mount(id)
}

window.vueMount = (id) => {
  const context = JSON.parse(document.getElementById(`${id}_vue_context`).textContent)
  updateContext(context)
  const component = components[context.vue_context.component]
  mount(component, '#' + id)
}

if (import.meta.env.DEV) {
  mount(App, '#app')
}
