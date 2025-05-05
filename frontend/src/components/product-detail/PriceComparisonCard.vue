<!-- frontend/src/components/product-detail/PriceComparisonCard.vue -->
<template>
    <v-card v-if="produto.tipo_produto === 'cliente'" elevation="2" class="mb-4 detail-card">
      <v-card-title class="primary--text">
        <v-icon left color="primary">mdi-compare</v-icon>
        Comparação de Preços
      </v-card-title>
      
      <v-card-text>
        <v-list>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-2 text-gray">Preço do Cliente</v-list-item-title>
              <v-list-item-subtitle class="text-h5 font-weight-medium primary--text mt-1">
                {{ formatarPreco(produto.preco_cliente) }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          
          <v-divider></v-divider>
          
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-2 text-gray">Menor Preço Concorrente</v-list-item-title>
              <v-list-item-subtitle class="text-h5 font-weight-medium mt-1">
                {{ formatarPreco(produto.menor_preco_concorrente) }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          
          <v-divider v-if="produto.diferenca_percentual !== null"></v-divider>
          
          <v-list-item v-if="produto.diferenca_percentual !== null">
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-2 text-gray">Diferença Percentual</v-list-item-title>
              <v-list-item-subtitle class="mt-1">
                <v-chip
                  :color="produto.diferenca_percentual <= 0 ? 'success' : 'error'"
                  class="font-weight-bold text-h6 px-4 py-2"
                  :text-color="produto.diferenca_percentual <= 0 ? 'white' : 'white'"
                  large
                >
                  {{ formatarPercentual(produto.diferenca_percentual) }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        
        <!-- Status visual de comparação -->
        <v-sheet 
          v-if="produto.diferenca_percentual !== null" 
          color="grey lighten-4" 
          class="pa-4 rounded mt-4"
        >
          <div class="text-center">
            <v-icon 
              :color="produto.diferenca_percentual <= 0 ? 'success' : 'error'"
              size="64"
            >
              {{ produto.diferenca_percentual <= 0 ? 'mdi-thumb-up' : 'mdi-thumb-down' }}
            </v-icon>
            <div class="text-subtitle-1 mt-2">
              {{ produto.diferenca_percentual <= 0 ? 'Seu preço está competitivo!' : 'Seu preço está acima da concorrência' }}
            </div>
          </div>
        </v-sheet>
        
        <!-- Alerta se não houver concorrentes -->
        <v-alert
          v-if="!produto.menor_preco_concorrente"
          type="info"
          class="mb-4 mt-4"
          outlined
          icon="mdi-alert-circle-outline"
        >
          <div class="text-subtitle-1 font-weight-medium mb-2">Sem Concorrentes Registrados</div>
          <p class="mb-0">Não há preços de concorrentes registrados para esse produto. Cadastre produtos concorrentes com o mesmo nome para habilitar a comparação.</p>
          <div class="mt-4">
            <v-btn
              color="primary"
              small
              outlined
              @click="$emit('add-competitor')"
            >
              <v-icon left small>mdi-plus</v-icon>
              Adicionar Concorrente
            </v-btn>
          </div>
        </v-alert>
      </v-card-text>
    </v-card>
  </template>
  
  <script setup>
  const props = defineProps({
    produto: {
      type: Object,
      required: true
    },
    formatarPreco: {
      type: Function,
      required: true
    },
    formatarPercentual: {
      type: Function,
      required: true
    }
  })
  
  const emit = defineEmits(['add-competitor'])
  </script>