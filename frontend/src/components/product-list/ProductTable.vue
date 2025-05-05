<!-- frontend/src/components/product-list/ProductTable.vue -->
<template>
    <v-card elevation="2" class="mb-4">
      <v-data-table
        :headers="headers"
        :items="produtos"
        :loading="loading"
        :search="search"
        :items-per-page="15"
        sort-by="nome"
        class="elevation-0 product-table"
        :loading-text="'Carregando produtos...'"
        :no-data-text="'Nenhum produto encontrado'"
        :footer-props="{
          'items-per-page-options': [10, 15, 20, 50],
          'items-per-page-text': 'Produtos por página'
        }"
      >
        <!-- Status do produto -->
        <template v-slot:item.tipo_produto="{ item }">
          <v-chip
            small
            :color="item.tipo_produto === 'cliente' ? 'primary' : 'grey lighten-1'"
            :text-color="item.tipo_produto === 'cliente' ? 'white' : 'grey darken-3'"
            class="px-2"
          >
            {{ item.tipo_produto === 'cliente' ? 'Cliente' : 'Concorrente' }}
          </v-chip>
        </template>
        
        <!-- Nome com tooltip para nomes longos -->
        <template v-slot:item.nome="{ item }">
          <v-tooltip bottom>
            <template v-slot:activator="{ props }">
              <span 
                v-bind="props"
                class="product-name-cell"
              >
                {{ item.nome }}
                <v-icon 
                  v-if="item.produto_cliente" 
                  small 
                  color="amber darken-2" 
                  class="ml-1"
                >
                  mdi-star
                </v-icon>
              </span>
            </template>
            <span>{{ item.nome }}</span>
          </v-tooltip>
        </template>
        
        <!-- URL com link clicável -->
        <template v-slot:item.url="{ item }">
          <v-tooltip bottom>
            <template v-slot:activator="{ props }">
              <div 
                v-bind="props"
                class="url-cell"
              >
                <a 
                  :href="item.url" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  class="text-decoration-none text-truncate d-block"
                >
                  {{ formatUrl(item.url) }}
                </a>
              </div>
            </template>
            <span>{{ item.url }}</span>
          </v-tooltip>
        </template>
        
        <!-- Status do tipo de verificação -->
        <template v-slot:item.verificacao_manual="{ item }">
          <v-tooltip bottom :color="item.verificacao_manual ? 'warning' : 'success'">
            <template v-slot:activator="{ props }">
              <v-icon 
                v-bind="props"
                :color="item.verificacao_manual ? 'warning' : 'success'"
              >
                {{ item.verificacao_manual ? 'mdi-hand' : 'mdi-robot' }}
              </v-icon>
            </template>
            <span>{{ item.verificacao_manual ? 'Verificação Manual' : 'Verificação Automática' }}</span>
          </v-tooltip>
        </template>
        
        <!-- Última verificação com formatação -->
        <template v-slot:item.ultima_verificacao="{ item }">
          <div class="d-flex align-center">
            <v-icon 
              small 
              :color="getVerificationStatusColor(item.ultima_verificacao)" 
              class="mr-2"
            >
              {{ getVerificationStatusIcon(item.ultima_verificacao) }}
            </v-icon>
            <span>{{ formatDate(item.ultima_verificacao) }}</span>
          </div>
        </template>
        
        <!-- Coluna de ações -->
        <template v-slot:item.actions="{ item }">
          <div class="actions-cell">
            <v-tooltip bottom>
              <template v-slot:activator="{ props }">
                <v-btn
                  icon
                  small
                  color="primary"
                  v-bind="props"
                  @click="$emit('view-details', item.id)"
                  class="mx-1"
                >
                  <v-icon>mdi-eye</v-icon>
                </v-btn>
              </template>
              <span>Ver detalhes</span>
            </v-tooltip>
            
            <v-tooltip bottom>
              <template v-slot:activator="{ props }">
                <v-btn
                  icon
                  small
                  color="success"
                  v-bind="props"
                  @click="$emit('verify-price', item.id)"
                  :loading="verificandoItem === item.id"
                  class="mx-1"
                >
                  <v-icon>mdi-refresh</v-icon>
                </v-btn>
              </template>
              <span>Verificar preço</span>
            </v-tooltip>
            
            <v-tooltip bottom>
              <template v-slot:activator="{ props }">
                <v-btn
                  icon
                  small
                  color="warning"
                  v-bind="props"
                  @click="$emit('edit-product', item.id)"
                  class="mx-1"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
              </template>
              <span>Editar produto</span>
            </v-tooltip>
          </div>
        </template>
        
        <!-- Status quando tabela estiver carregando -->
        <template v-slot:progress>
          <v-overlay :value="loading" absolute color="white" opacity="0.8">
            <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          </v-overlay>
        </template>
      </v-data-table>
    </v-card>
  </template>
  
  <script setup>
  const props = defineProps({
    headers: {
      type: Array,
      required: true
    },
    produtos: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    },
    search: {
      type: String,
      default: ''
    },
    verificandoItem: {
      type: [String, Number, null],
      default: null
    },
    formatUrl: {
      type: Function,
      required: true
    },
    formatDate: {
      type: Function,
      required: true
    },
    getVerificationStatusColor: {
      type: Function,
      required: true
    },
    getVerificationStatusIcon: {
      type: Function,
      required: true
    }
  })
  
  const emit = defineEmits(['view-details', 'verify-price', 'edit-product'])
  </script>
  
  <style scoped>
  .product-table {
    border-radius: 8px;
    overflow: hidden;
  }
  
  :deep(.v-data-table th) {
    font-weight: bold !important;
    color: rgba(0, 0, 0, 0.7) !important;
    background-color: #f5f5f5;
    text-transform: uppercase;
    font-size: 0.75rem;
  }
  
  :deep(.v-data-table tr:hover) {
    background-color: #f5f7fa !important;
  }
  
  :deep(.v-data-table tr:nth-child(even)) {
    background-color: #fafafa;
  }
  
  .product-name-cell {
    font-weight: 500;
    color: var(--v-primary-base);
    display: block;
    max-width: 200px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .url-cell {
    max-width: 200px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .actions-cell {
    display: flex;
    justify-content: center;
  }
  
  .v-chip {
    font-size: 0.75rem !important;
  }
  </style>