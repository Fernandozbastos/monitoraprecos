<template>
    <v-card class="mb-4 stats-card" elevation="3" rounded="lg">
      <v-card-text class="pa-4">
        <div class="d-flex align-center">
          <div :class="`rounded-circle ${color} pa-4 mr-4`">
            <v-icon color="white" size="32">{{ icon }}</v-icon>
          </div>
          <div>
            <div class="text-overline text-grey">{{ title }}</div>
            <div class="text-h4 font-weight-bold">{{ value }}</div>
          </div>
        </div>
      </v-card-text>
    </v-card>
  </template>
  
  <script setup>
  defineProps({
    title: {
      type: String,
      required: true
    },
    value: {
      type: [String, Number],
      required: true
    },
    icon: {
      type: String,
      required: true
    },
    color: {
      type: String,
      default: 'primary',
      validator: (value) => {
        return ['primary', 'info', 'success', 'warning', 'error'].includes(value)
      }
    }
  })
  </script>
  
  <style scoped>
  .stats-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-radius: 8px;
    overflow: hidden;
  }
  
  .stats-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
  }
  
  .rounded-circle {
    border-radius: 50% !important;
  }
  </style>