<!-- frontend/src/components/product-detail/PriceHistoryChart.vue -->
<template>
    <v-card elevation="2" class="mb-4">
      <v-card-title class="primary--text">
        <v-icon left color="primary">mdi-chart-line</v-icon>
        Histórico de Preços
        <v-spacer></v-spacer>
        <v-btn
          small
          outlined
          color="primary"
          :loading="carregandoHistorico"
          @click="$emit('refresh')"
        >
          <v-icon left small>mdi-refresh</v-icon>
          Atualizar Histórico
        </v-btn>
      </v-card-title>
      
      <v-card-text>
        <loading-spinner
          v-if="carregandoHistorico"
          :loading="true"
          text="Carregando histórico..."
        />
        
        <div v-else-if="historicoPrecos.length === 0" class="text-center py-8">
          <v-icon size="64" color="grey lighten-1">mdi-chart-timeline-variant</v-icon>
          <h3 class="text-h6 grey--text text--darken-1 mt-4">Nenhum histórico de preço encontrado</h3>
          <p class="text-body-2 grey--text">Verificar o preço deste produto para começar a monitorá-lo</p>
          <v-btn
            color="primary"
            class="mt-4"
            @click="$emit('verify-price')"
          >
            <v-icon left>mdi-refresh</v-icon>
            Verificar Preço
          </v-btn>
        </div>
        
        <div v-else ref="chartContainer" style="height: 400px; width: 100%;" class="chart-container">
          <canvas ref="priceChart"></canvas>
        </div>
      </v-card-text>
    </v-card>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
  
  const props = defineProps({
    carregandoHistorico: {
      type: Boolean,
      default: false
    },
    historicoPrecos: {
      type: Array,
      default: () => []
    }
  })
  
  const emit = defineEmits(['refresh', 'verify-price'])
  
  // Refs para o gráfico
  const priceChart = ref(null)
  const chartContainer = ref(null)
  
  // Expor refs para uso externo
  defineExpose({
    priceChart,
    chartContainer
  })
  </script>
  
  <style scoped>
  .chart-container {
    position: relative;
    margin: auto;
    height: 400px;
    width: 100%;
  }
  
  canvas {
    max-width: 100%;
    max-height: 400px;
  }
  </style>