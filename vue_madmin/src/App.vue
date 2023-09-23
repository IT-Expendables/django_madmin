<script setup>
import HomeView from '@/views/HomeView.vue'
import MFileUpload from '@/views/MFileUpload.vue'
import MMultiFileUpload from '@/views/MMultiFileUpload.vue'
</script>

<template>
  <div class="flex flex-col gap-y-4">
    <HomeView />
    <MFileUpload />
    <MMultiFileUpload />
  </div>
</template>
