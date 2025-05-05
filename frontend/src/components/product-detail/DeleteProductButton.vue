<!-- frontend/src/components/product-detail/DeleteProductButton.vue -->
<template>
    <v-btn 
      color="error"
      :outlined="outlined"
      :loading="deletingLoading"
      @click="handleDelete"
      :disabled="disabled"
    >
      <v-icon left>mdi-delete</v-icon>
      {{ buttonText }}
    </v-btn>
  </template>
  
  <script setup>
  import { defineProps, defineEmits } from 'vue'
  
  const props = defineProps({
    outlined: {
      type: Boolean,
      default: false
    },
    buttonText: {
      type: String,
      default: 'Excluir'
    },
    disabled: {
      type: Boolean,
      default: false
    },
    deletingLoading: {
      type: Boolean,
      default: false
    }
  })
  
  const emit = defineEmits(['delete'])
  
  const handleDelete = () => {
    emit('delete')
  }
  </script>