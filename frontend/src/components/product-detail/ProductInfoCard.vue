<!-- frontend/src/components/product-detail/ProductInfoCard.vue -->
<template>
    <v-card elevation="2" class="mb-4 detail-card">
      <v-card-title class="primary--text">
        <v-icon left color="primary">mdi-information-outline</v-icon>
        Informações do Produto
      </v-card-title>
      
      <v-card-text>
        <v-list>
          <v-list-item two-line>
            <v-list-item-avatar color="primary" class="rounded white--text">
              <v-icon>mdi-tag</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-2 text-gray">Nome</v-list-item-title>
              <v-list-item-subtitle class="text-h6">{{ produto.nome || 'N/A' }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
          
          <v-list-item two-line>
            <v-list-item-avatar color="info" class="rounded white--text">
              <v-icon>mdi-store</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-2 text-gray">
                {{ produto.tipo_produto === 'cliente' ? 'Tipo' : 'Concorrente' }}
              </v-list-item-title>
              <v-list-item-subtitle class="text-h6">
                {{ produto.tipo_produto === 'cliente' ? 'Produto do Cliente' : produto.concorrente || 'N/A' }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
          
          <v-list-item two-line>
            <v-list-item-avatar color="warning" class="rounded white--text">
              <v-icon>mdi-link-variant</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-2 text-gray">URL</v-list-item-title>
              <v-list-item-subtitle style="word-break: break-all;">
                <a 
                  v-if="produto.url"
                  :href="produto.url" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  class="text-decoration-none"
                >
                  {{ produto.url }}
                </a>
                <span v-else>N/A</span>
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
          
          <v-list-item two-line>
            <v-list-item-avatar color="success" class="rounded white--text">
              <v-icon>mdi-web</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-2 text-gray">Plataforma</v-list-item-title>
              <v-list-item-subtitle>{{ produto.plataforma?.nome || 'N/A' }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
          
          <v-list-item two-line>
            <v-list-item-avatar color="error" class="rounded white--text">
              <v-icon>mdi-clock-outline</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-2 text-gray">Última Verificação</v-list-item-title>
              <v-list-item-subtitle>{{ formatDate(produto.ultima_verificacao) }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </template>
  
  <script setup>
  const props = defineProps({
    produto: {
      type: Object,
      required: true
    },
    formatDate: {
      type: Function,
      required: true
    }
  })
  </script>
  
  <style scoped>
  .text-gray {
    color: rgba(0, 0, 0, 0.6);
  }
  
  .rounded {
    border-radius: 50%;
  }
  
  .detail-card {
    border-radius: 8px;
    overflow: hidden;
    transition: all 0.3s ease;
  }
  
  .detail-card:hover {
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
  }
  
  :deep(.v-list-item__avatar) {
    margin-right: 16px !important;
  }
  
  :deep(.v-list-item) {
    padding: 16px !important;
  }
  </style>