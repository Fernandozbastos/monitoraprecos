<template>
    <v-data-table
      :headers="headers"
      :items="produtos"
      :items-per-page="5"
      class="elevation-0 product-table"
      hide-default-footer
      dense
    >
      <!-- Tipo de produto -->
      <template v-slot:item.tipo_produto="{ item }">
        <v-chip
          :color="item.tipo_produto === 'cliente' ? 'primary' : 'grey lighten-3'"
          small
          :text-color="item.tipo_produto === 'cliente' ? 'white' : 'grey darken-2'"
        >
          {{ item.tipo_produto === 'cliente' ? 'Cliente' : 'Concorrente' }}
        </v-chip>
      </template>
      
      <!-- Concorrente -->
      <template v-slot:item.concorrente="{ item }">
        <span :class="{'font-weight-bold': item.tipo_produto === 'cliente'}">
          {{ item.concorrente }}
          <span v-if="item.produto_cliente" class="ml-1 caption font-italic">(Produto Cliente)</span>
        </span>
      </template>
      
      <!-- Produto Cliente Base -->
      <template v-slot:item.produto_cliente="{ item }">
        <v-icon v-if="item.produto_cliente" color="primary">mdi-star</v-icon>
        <v-icon v-else color="grey lighten-1">mdi-star-outline</v-icon>
      </template>
      
      <!-- Preço -->
      <template v-slot:item.preco="{ item }">
        <span :class="{'primary--text font-weight-bold': item.produto_cliente}">
          {{ formatarPreco(getPreco(item)) }}
        </span>
      </template>
      
      <!-- Diferença percentual -->
      <template v-slot:item.diferenca_percentual="{ item }">
        <v-chip
          v-if="item.diferenca_percentual !== null"
          :color="getCorDiferenca(item.diferenca_percentual)"
          small
          dark
        >
          {{ formatarPercentual(item.diferenca_percentual) }}
        </v-chip>
        <span v-else class="text-caption grey--text">N/A</span>
      </template>
      
      <!-- Data da verificação -->
      <template v-slot:item.ultima_verificacao="{ item }">
        <div class="d-flex align-center">
          <v-icon small class="mr-1" :color="item.ultima_verificacao ? 'success' : 'grey'">
            {{ item.ultima_verificacao ? 'mdi-clock-check-outline' : 'mdi-clock-alert-outline' }}
          </v-icon>
          <span class="text-caption">{{ formatDate(item.ultima_verificacao) }}</span>
        </div>
      </template>
      
      <!-- Ações -->
      <template v-slot:item.actions="{ item }">
        <div class="d-flex">
          <v-tooltip location="bottom">
            <template v-slot:activator="{ props }">
              <v-btn
                icon
                x-small
                color="primary"
                class="mr-1"
                @click="$emit('view-details', item.id)"
                v-bind="props"
              >
                <v-icon>mdi-eye</v-icon>
              </v-btn>
            </template>
            <span>Ver detalhes</span>
          </v-tooltip>
  
          <v-tooltip location="bottom">
            <template v-slot:activator="{ props }">
              <v-btn
                icon
                x-small
                color="success"
                @click="$emit('verify-price', item.id)"
                :loading="verificandoItem === item.id"
                v-bind="props"
              >
                <v-icon>mdi-refresh</v-icon>
              </v-btn>
            </template>
            <span>Verificar preço</span>
          </v-tooltip>
          
          <v-tooltip location="bottom">
            <template v-slot:activator="{ props }">
              <v-btn
                icon
                x-small
                color="warning"
                class="ml-1"
                @click="$emit('set-base', item)"
                :disabled="item.produto_cliente"
                v-bind="props"
              >
                <v-icon>mdi-star</v-icon>
              </v-btn>
            </template>
            <span>Definir como produto cliente base</span>
          </v-tooltip>
  
          <v-tooltip location="bottom">
            <template v-slot:activator="{ props }">
              <v-btn
                icon
                x-small
                color="error"
                class="ml-1"
                @click="$emit('delete', item)"
                v-bind="props"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
            <span>Excluir produto</span>
          </v-tooltip>
        </div>
      </template>
    </v-data-table>
  </template>
  
  <script setup>
  import { formatarPreco, formatarPercentual, formatDate, getCorDiferenca } from '@/utils/formatters'
  
  const props = defineProps({
    produtos: {
      type: Array,
      required: true
    },
    getPreco: {
      type: Function,
      required: true
    },
    verificandoItem: {
      type: [String, Number, null],
      default: null
    }
  })
  
  defineEmits(['view-details', 'verify-price', 'set-base', 'delete'])
  
  const headers = [
    { text: 'Tipo', value: 'tipo_produto', width: '100px' },
    { text: 'Base', value: 'produto_cliente', width: '80px', align: 'center' },
    { text: 'Empresa', value: 'concorrente' },
    { text: 'Preço', value: 'preco', width: '120px' },
    { text: 'Diferença', value: 'diferenca_percentual', width: '120px' },
    { text: 'Última Verificação', value: 'ultima_verificacao', width: '180px' },
    { text: 'Ações', value: 'actions', align: 'center', sortable: false, width: '140px' }
  ]
  </script>
  
  <style scoped>
  .product-table {
    border-radius: 4px;
    overflow: hidden;
  }
  
  :deep(.v-data-table th) {
    font-weight: bold !important;
    color: rgba(0, 0, 0, 0.7) !important;
    background-color: #fafafa;
  }
  
  :deep(.v-data-table tr:hover) {
    background-color: #f5f7fa !important;
  }
  
  :deep(.v-data-table tr:nth-child(even)) {
    background-color: #fcfcfc;
  }
  </style>