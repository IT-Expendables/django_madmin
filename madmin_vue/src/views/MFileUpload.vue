<script setup>
import { computed, ref } from 'vue'
import { PlusOutlined, FileTwoTone, DeleteOutlined, EyeOutlined, PlayCircleTwoTone } from '@ant-design/icons-vue'
import { Modal as AModal, Progress as AProgress, Image as AImage } from 'ant-design-vue'
import { useUpload } from '@/managers/upload'
import { vueContextRef, contextRef } from '@/managers/context'

const uploadTypeRef = computed(() => vueContextRef.value.upload_type || 'file')

const { host, fileInfoRef, open, clear, progressRef, localURLRef } = useUpload()

const preview = ref(false)

const onPreview = async () => {
  if (uploadTypeRef.value == 'image') return
  const { url } = fileInfoRef.value || {}
  if (!url) return
  if (uploadTypeRef.value == 'video') {
    preview.value = true
  } else {
    window.open(host + url)
  }
}
</script>

<template>
  <div
    class="w-24 h-24 p-2 rounded border border-gray-300 group"
    :class="!fileInfoRef ? 'border-dashed hover:border-blue-400 transition-all' : ''"
  >
    <input v-if="contextRef.name" :name="contextRef.name" :value="fileInfoRef && fileInfoRef.url" class="hidden" />
    <div
      v-if="!fileInfoRef"
      class="w-full h-full cursor-pointer flex flex-col items-center justify-center"
      @click="open()"
    >
      <PlusOutlined />
      <div>点击上传</div>
    </div>
    <div
      v-else
      class="w-full h-full flex flex-col items-center justify-center cursor-pointer relative"
      @click="onPreview"
    >
      <div v-if="uploadTypeRef == 'image'" class="w-full h-full bg-gray-100 flex items-center">
        <AImage :width="100" :height="100" :src="host + fileInfoRef.url || localURLRef">
          <template #previewMask>
            <EyeOutlined />
          </template>
        </AImage>
      </div>
      <template v-else>
        <PlayCircleTwoTone v-if="uploadTypeRef == 'video'" class="text-[30px]" />
        <FileTwoTone v-else class="text-[30px]" />
        <div class="line-clamp-2 text-xs mt-1 break-all text-center">{{ fileInfoRef.name }}</div>
      </template>
      <div
        v-if="fileInfoRef && fileInfoRef.status == 'uploading'"
        class="absolute top-0 left-0 w-full h-full bg-black bg-opacity-60 flex items-center justify-center"
      >
        <AProgress type="circle" :size="50" trail-color="white" :show-info="false" :percent="progressRef" />
      </div>
      <DeleteOutlined
        v-if="fileInfoRef && fileInfoRef.status != 'uploading'"
        class="cursor-pointer text-gray-400 hover:text-gray-500 transition-all absolute -top-1 -right-1"
        @click="clear()"
      />
    </div>
  </div>
  <AModal
    :open="preview"
    :footer="null"
    :closable="false"
    @cancel="preview = false"
    :destroyOnClose="true"
    width="80vw"
    height="80vh"
  >
    <video controls class="h-[calc(80vh-40px)] w-[calc(80vw-48px)]" :src="host + fileInfoRef.url" />
  </AModal>
</template>
