<!-- frontend/src/components/product-detail/ProductDetailHeader.vue -->
<template>
    <div>
      <!-- Botão de navegação com melhor visual -->
      <v-btn 
        text 
        class="mb-4 pl-0 transition-swing"
        @click="$emit('back')"
      >
        <v-icon left>mdi-arrow-left</v-icon>
        Voltar para a lista
      </v-btn>
      
      <!-- Cabeçalho do produto -->
      <v-card elevation="3" class="mb-6 gradient-header">
        <v-card-text class="pa-6">
          <div class="d-flex flex-wrap align-center">
            <div>
              <h1 class="text-h4 white--text mb-1">{{ produto.nome || 'Detalhes do Produto' }}</h1>
              <p class="text-subtitle-1 white--text mb-0">
                {{ produto.tipo_produto === 'cliente' ? 'Produto do Cliente' : 'Produto do Concorrente' }}
                <v-chip
                  v-if="produto.produto_cliente"
                  small
                  color="amber"
                  text-color="black"
                  class="ml-2"
                >
                  <v-icon left small>mdi-star</v-icon>
                  Produto Base
                </v-chip>
              </p>
            </div>
            
            <v-spacer></v-spacer>
            
            <div>
              <v-btn 
                color="white" 
                class="primary--text mr-2"
                :loading="verificando"
                @click="$emit('verify-price')"
              >
                <v-icon left>mdi-refresh</v-icon>
                Verificar Preço
              </v-btn>
              
              <v-btn 
                v-if="produto.url"
                text
                color="white"
                class="ml-2"
                :href="produto.url" 
                target="_blank"
              >
                <v-icon left>mdi-open-in-new</v-icon>
                Abrir Site
              </v-btn>
              
              <!-- Botão de exclusão -->
              <delete-product-button
                class="ml-2"
                :deleting-loading="false"
                @delete="$emit('delete')"
              />
            </div>
          </div>
        </v-card-text>
      </v-card>
    </div>
  </template>
  
  <script setup>
  import DeleteProductButton from './DeleteProductButton.vue'
  
  const props = defineProps({
    produto: {
      type: Object,
      required: true
    },
    verificando: {
      type: Boolean,
      default: false
    }
  })
  
  const emit = defineEmits(['back', 'verify-price', 'delete'])
  </script>
  
  <style scoped>
  .gradient-header {
    background: linear-gradient(135deg, var(--v-primary-base) 0%, var(--v-primary-darken1) 100%);
    border-radius: 8px;
    color: white;
  }
  
  .transition-swing {
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
  }
  
  .transition-swing:hover {
    transform: translateX(-4px);
  }
  </style>