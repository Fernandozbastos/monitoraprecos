<!-- frontend/src/components/product-list/ProductListHeader.vue -->
<template>
    <v-card elevation="3" class="mb-6 gradient-header">
      <v-card-text class="pa-6">
        <div class="d-flex flex-wrap align-center">
          <div>
            <h1 class="text-h4 white--text mb-1">Produtos</h1>
            <p class="text-subtitle-1 white--text mb-0">Gerencie seus produtos e concorrentes</p>
          </div>
          <v-spacer></v-spacer>
          <div>
            <v-btn
              color="white"
              class="primary--text text-none px-4 mr-2"
              :loading="loading"
              @click="$emit('refresh')"
            >
              <v-icon left>mdi-refresh</v-icon>
              Atualizar
            </v-btn>
            <v-btn
              color="success"
              dark
              elevation="1"
              class="text-none px-4"
              @click="$emit('add-product')"
            >
              <v-icon left>mdi-plus</v-icon>
              Adicionar Produto
            </v-btn>
          </div>
        </div>
      </v-card-text>
    </v-card>
  </template>
  
  <script setup>
  const props = defineProps({
    loading: {
      type: Boolean,
      default: false
    }
  })
  
  const emit = defineEmits(['refresh', 'add-product'])
  </script>
  
  <style scoped>
  .gradient-header {
    background: linear-gradient(135deg, var(--v-primary-base) 0%, var(--v-primary-darken1) 100%);
    border-radius: 8px;
  }
  </style>