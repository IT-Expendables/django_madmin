<script setup>
import axios from "axios"
import { computed, ref } from "vue"
import { UploadDragger as AUploadDragger, message } from "ant-design-vue"
import { InboxOutlined } from "@ant-design/icons-vue"
import { calcFileHash, URL } from '@/utils'

const DEBUG = import.meta.env.DEV

const props = defineProps({
  context: { type: Object, default: () => ({}) }
})

const { name, value: defaultValue = '', max_num = 5, file_limit = 500, check_upload_url: checkURL, upload_dir: dir } = props.context

const defaultFiles = !defaultValue || defaultValue == '' ? [] : defaultValue.split(',').map(e => ({ url: e, name: decodeURIComponent(e.split('/').reverse()[0]) }))

const uploadUrlRef = ref('')
const uploadDataRef = ref({})

const fileListRef = ref(defaultFiles)

const fileUrlsRef = computed(() =>
  fileListRef.value.filter(f => f.status != 'uploading' && f.status != 'error').map(f => f.url)
)

const beforeUpload = async file => {
  if (fileListRef.value.length >= max_num) {
    file.status = 'error'
    file.response = `最多上传${max_num}个文件`
    message.error(`最多上传${max_num}个文件`)
    return false
  }
  else if (file.size / 1024 / 1024 > file_limit) {
    file.status = 'error'
    file.response = `请选择小于${file_limit}M的文件上传`
    message.error(`请选择小于${file_limit}M的文件上传`)
    return false
  }
  const name = file.name
  const hash = await calcFileHash(file)
  try {
    const res = await axios.post(URL(checkURL), { name, hash, dir })
    DEBUG && console.log('check upload success: ', res.data)
    const { file_url, upload_url } = res.data
    if (file_url && file_url != '') {
      file.url = URL(file_url)
      file.status = 'done'
      return false
    }
    if (upload_url && upload_url != '') {
      uploadDataRef.value = { hash, name: file.name, dir }
      uploadUrlRef.value = URL(upload_url)
      return true
    }
  } catch (err) {
    DEBUG && console.log('check upload error: ', err)
    err.response && err.response.data && message.error(err.response.data)
    file.status = 'error'
    file.response = err.response && err.response.data || '上传失败'
  }
  return false
}

const handleChange = ({ file }) => {
  if (file.status === 'done') {
    const { file_url } = file.response || {}
    file.url = URL(file_url)
  }
}

</script>

<template>
  <AUploadDragger v-model:fileList="fileListRef" name="file" :multiple="true" :data="uploadDataRef" :action="uploadUrlRef"
    :before-upload="beforeUpload" @change="handleChange">
    <input v-if="name" :name="name" :value="fileUrlsRef" class="hidden" />
    <InboxOutlined class=" text-[52px] text-[--theme]" />
    <p class="mt-2 text-xs text-[#666]">点击或将文件拖拽到这里上传</p>
  </AUploadDragger>
</template>
