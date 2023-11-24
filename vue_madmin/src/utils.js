import SparkMD5 from 'spark-md5'

const DEBUG = import.meta.env.DEV

export const calcFileHash = (file) => {
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
        resolve(md5.slice(0, 8))
      }
    }
    fileReader.onerror = () => {
      resolve()
    }
    loadNextChunk()
  })
}

export function URL(str) {
  const host = DEBUG ? 'http://127.0.0.1:8000' : ''
  return host + str
}


window.calcFileHash = calcFileHash
