<!-- frontend/src/components/common/LoadingSpinner.vue -->
<template>
    <div class="loading-spinner-container" v-if="isLoading">
      <div class="spinner-overlay" :style="{ background: overlayColor }">
        <v-progress-circular
          :indeterminate="indeterminate"
          :value="progress"
          :size="size"
          :width="width"
          :color="color"
          :rotate="rotate"
        ></v-progress-circular>
        <div v-if="text" class="loading-text mt-4" :style="{ color: textColor }">
          {{ text }}
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    loading: {
      type: Boolean,
      default: false
    },
    size: {
      type: [Number, String],
      default: 64
    },
    width: {
      type: [Number, String],
      default: 7
    },
    color: {
      type: String,
      default: 'primary'
    },
    text: {
      type: String,
      default: ''
    },
    textColor: {
      type: String,
      default: '#1976d2'
    },
    overlayColor: {
      type: String,
      default: 'rgba(255, 255, 255, 0.9)'
    },
    indeterminate: {
      type: Boolean,
      default: true
    },
    progress: {
      type: Number,
      default: 0
    },
    rotate: {
      type: Number,
      default: 360
    },
    fullscreen: {
      type: Boolean,
      default: false
    }
  })
  
  const isLoading = computed(() => props.loading)
  </script>
  
  <style scoped>
  .loading-spinner-container {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
  }
  
  .spinner-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 10;
    backdrop-filter: blur(2px);
    -webkit-backdrop-filter: blur(2px);
  }
  
  /* Para uso em fullscreen */
  .fullscreen .loading-spinner-container {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 9999;
  }
  
  .loading-text {
    font-size: 1rem;
    text-align: center;
    white-space: nowrap;
  }
  
  /* Ansimates spin para efeito visual */
  .v-progress-circular {
    animation: rotate 2s linear infinite;
  }
  
  @keyframes rotate {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
  </style>