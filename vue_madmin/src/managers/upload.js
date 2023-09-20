import { ref, computed } from 'vue'
import { useFileDialog, useObjectUrl } from '@vueuse/core'
import axios from 'axios'
import SparkMD5 from 'spark-md5'
import { message } from 'ant-design-vue'

const DEBUG = import.meta.env.DEV

export function useUpload({context}) {
  const vueContext = (context || {}).vue_context || {}

  const host = DEBUG ? 'http://127.0.0.1:8000' : ''

  const checkURL = vueContext.check_upload_url || '/madmin/check_upload/'

  const fileInfoRef = ref(context.value ? { url: context.value } : null)

  const progressRef = ref(0)

  const fileRef = computed(() => fileInfoRef.value && fileInfoRef.value.file)
  const localURLRef = useObjectUrl(fileRef)

  const { open, reset, onChange: onFileChange } = useFileDialog()

  const calcMD5 = (file) => {
    return new Promise((resolve) => {
      const chunkSize = 8192
      const fileReader = new FileReader()
      const spark = new SparkMD5.ArrayBuffer()
      const chunks = Math.ceil(file.size / chunkSize)
      let currentChunk = 0
      const loadNextChunk = () => {
        const start = currentChunk * chunkSize
        const end = Math.min(file.size, start + chunkSize)
        const chunk = file.slice(start, end)
        fileReader.readAsArrayBuffer(chunk)
      }
      fileReader.onload = (event) => {
        spark.append(event.target.result)
        currentChunk++
        if (currentChunk < chunks) {
          loadNextChunk()
        } else {
          const md5 = spark.end()
          resolve(md5)
        }
      }
      fileReader.onerror = () => {
        resolve()
      }
      loadNextChunk()
    })
  }

  const checkUpload = async (file, hash) => {
    try {
      const name = file.name
      const response = await axios.post(checkURL, { hash, name })
      const res = response.data
      DEBUG && console.log('check upload success: ', res)
      return res
    } catch (err) {
      DEBUG && console.log('check upload error: ', err)
      err.data && message.error(err.data)
    }
  }

  const onUploadProgress = ({ progress }) => {
    progressRef.value = parseInt(progress * 100)
  }

  const upload = async (upload_url, file, hash) => {
    try {
      const response = await axios.post(
        upload_url,
        { hash, file },
        { headers: { 'Content-Type': 'multipart/form-data;' }, onUploadProgress }
      )
      const res = response.data || {}
      DEBUG && console.log('upload success: ', res)
      return res
    } catch (err) {
      DEBUG && console.log('upload error: ', err)
      err.data && message.error(err.data)
    }
  }

  const startUpload = async (file) => {
    fileInfoRef.value = { name: file.name, file, status: 'uploading' }
    const hash = await calcMD5(file)
    if (!hash) {
      fileInfoRef.value.status = 'error'
      message.error('上传文件错误')
      return
    }
    const { file_url, upload_url } = await checkUpload(file, hash)
    if (file_url && file_url != '') {
      fileInfoRef.value = { url: file_url, name: file.name, file, status: 'success' }
      return
    }
    if (upload_url && upload_url != '') {
      const { file_url } = (await upload(host + upload_url, file, hash)) || {}
      if (file_url) {
        fileInfoRef.value = { url: file_url, name: file.name, file, status: 'success' }
        return
      }
      fileInfoRef.value.status = 'error'
    }
  }

  const clear = () => {
    fileInfoRef.value = null
    progressRef.value = 0
  }

  onFileChange((files) => {
    if (!files.length) return
    const file = files[0]
    startUpload(file)
    reset()
  })

  return { host, fileInfoRef, open, clear, progressRef, localURLRef }
}
