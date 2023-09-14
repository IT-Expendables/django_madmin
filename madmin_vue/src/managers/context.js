import { ref, computed } from 'vue'

const contextRef = ref({})

const vueContextRef = computed(() => contextRef.value.vue_context || {})

const updateContext = (context) => {
  contextRef.value = context || {}
}

export { updateContext, contextRef, vueContextRef }
