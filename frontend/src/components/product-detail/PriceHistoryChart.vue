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
        <!-- Debug info -->
        <v-alert 
          v-if="debugInfo" 
          type="info" 
          dense 
          class="mb-2"
        >
          {{ debugInfo }}
        </v-alert>
        
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
        
        <div v-else style="position: relative;">
          <!-- Canvas container com tamanho fixo -->
          <div 
            ref="chartContainer" 
            style="width: 100%; height: 400px; position: relative;"
          >
            <canvas 
              ref="priceChart"
              :id="chartId"
              style="width: 100% !important; height: 400px !important;"
            ></canvas>
          </div>
          
          <!-- Debug info para dimensões -->
          <div class="caption text-grey mt-2">
            Container: {{ containerDimensions.width }}x{{ containerDimensions.height }}
          </div>
        </div>
      </v-card-text>
    </v-card>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted, watch } from 'vue'
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
  const chartId = ref(`chart-${Math.random().toString(36).substr(2, 9)}`)
  
  // Debug
  const debugInfo = ref('')
  const containerDimensions = ref({ width: 0, height: 0 })
  
  // Verificar dimensões do container
  const checkDimensions = () => {
    if (chartContainer.value) {
      const rect = chartContainer.value.getBoundingClientRect()
      containerDimensions.value = {
        width: rect.width,
        height: rect.height
      }
      debugInfo.value = `Canvas ref: ${priceChart.value ? 'OK' : 'NULL'}, Container: ${rect.width}x${rect.height}`
    }
  }
  
  // Watch para mudanças no histórico
  watch(() => props.historicoPrecos, (newValue) => {
    debugInfo.value = `Histórico atualizado: ${newValue.length} registros`
    checkDimensions()
  })
  
  // Verificar se canvas está disponível
  const verificarCanvas = () => {
    if (priceChart.value) {
      debugInfo.value += ' | Canvas encontrado'
      if (priceChart.value.getContext) {
        debugInfo.value += ' | Context disponível'
      } else {
        debugInfo.value += ' | Context INDISPONÍVEL'
      }
    } else {
      debugInfo.value += ' | Canvas NÃO encontrado'
    }
  }
  
  // Lifecycle hooks
  onMounted(() => {
    checkDimensions()
    verificarCanvas()
    
    // Verificar disponibilidade após um tick
    setTimeout(() => {
      verificarCanvas()
      checkDimensions()
    }, 100)
  })
  
  onUnmounted(() => {
    debugInfo.value = 'Componente desmontado'
  })
  
  // Expor refs para uso externo
  defineExpose({
    priceChart,
    chartContainer,
    checkDimensions
  })
  </script>
  
  <style scoped>
  /* Garantir que o container tenha tamanho */
  :deep(.v-card-text) {
    min-height: 450px;
  }
  
  canvas {
    display: block;
  }
  </style>