<!-- frontend/src/views/ProductDetail.vue -->
<template>
    <v-container fluid>
      <!-- Estado de carregamento -->
      <loading-spinner 
        v-if="loading" 
        :loading="true" 
        text="Carregando detalhes do produto..."
      />
      
      <template v-else>
        <!-- Cabeçalho -->
        <product-detail-header
          :produto="produto"
          :verificando="verificando"
          @back="$router.go(-1)"
          @verify-price="verificarPreco"
          @delete="excluirProduto"
        />
        
        <v-row>
          <!-- Coluna de informações do produto -->
          <v-col cols="12" md="6">
            <product-info-card
              :produto="produto"
              :format-date="formatDate"
            />
          </v-col>
          
          <v-col cols="12" md="6">
            <!-- Preço do Cliente (apenas para produtos do cliente) -->
            <client-price-card
              v-if="produto.tipo_produto === 'cliente'"
              :produto="produto"
              v-model:preco-cliente="precoCliente"
              v-model:form-valid="formValid"
              :atualizando-preco="atualizandoPreco"
              :preco-rules="precoRules"
              @submit="atualizarPrecoCliente"
            />
            
            <!-- Comparação de Preços (apenas para produtos do cliente) -->
            <price-comparison-card
              v-if="produto.tipo_produto === 'cliente'"
              :produto="produto"
              :formatar-preco="formatarPreco"
              :formatar-percentual="formatarPercentual"
              @add-competitor="$router.push('/products/add')"
            />
            
            <!-- Configurações do produto -->
            <product-settings-card
              :produto="produto"
              :atualizando-status="atualizandoStatus"
              :corrigindo-tipo="corrigindoTipo"
              :formatar-preco="formatarPreco"
              @update-status="atualizarProdutoClienteStatus"
              @corrigir-tipo="corrigirTipoProduto"
            />
          </v-col>
        </v-row>
  
        <!-- Gráfico de histórico de preços -->
        <v-row>
          <v-col cols="12">
            <price-history-chart
              :carregando-historico="carregandoHistorico"
              :historico-precos="historicoPrecos"
              @refresh="carregarHistorico"
              @verify-price="verificarPreco"
              ref="priceChartComponent"
            />
          </v-col>
        </v-row>
      </template>
      
      <!-- Snackbar para mensagens de sucesso/erro -->
      <custom-snackbar />
    </v-container>
  </template>
  
  <script setup>
  import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
  import { useRouter } from 'vue-router'
  
  // Composables
  import { useProductDetail } from '@/composables/useProductDetail'
  import { usePriceHistory } from '@/composables/usePriceHistory'
  
  // Componentes
  import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
  import ProductDetailHeader from '@/components/product-detail/ProductDetailHeader.vue'
  import ProductInfoCard from '@/components/product-detail/ProductInfoCard.vue'
  import ClientPriceCard from '@/components/product-detail/ClientPriceCard.vue'
  import PriceComparisonCard from '@/components/product-detail/PriceComparisonCard.vue'
  import ProductSettingsCard from '@/components/product-detail/ProductSettingsCard.vue'
  import PriceHistoryChart from '@/components/product-detail/PriceHistoryChart.vue'
  import CustomSnackbar from '@/components/common/CustomSnackbar.vue'
  
  const router = useRouter()
  
  // Usar o composable do ProductDetail
  const {
    loading,
    produto,
    precoCliente,
    formValid,
    form,
    verificando,
    atualizandoPreco,
    atualizandoStatus,
    corrigindoTipo,
    precoRules,
    formatDate,
    formatarPreco,
    formatarPercentual,
    verificarPreco,
    atualizarPrecoCliente,
    atualizarProdutoClienteStatus,
    corrigirTipoProduto,
    excluirProduto,
    carregarProduto
  } = useProductDetail()
  
  // Usar o composable do histórico de preços
  const {
    historicoPrecos,
    carregandoHistorico,
    priceChart,
    chartContainer,
    carregarHistoricoCompleto,
    atualizarTituloGrafico,
    resizeChart
  } = usePriceHistory()
  
  // Referência para o componente de gráfico
  const priceChartComponent = ref(null)
  
  // Conectar refs do gráfico
  const conectarRefsGrafico = () => {
    nextTick(() => {
      if (priceChartComponent.value) {
        const { priceChart: chartRef, chartContainer: containerRef } = priceChartComponent.value
        priceChart.value = chartRef
        chartContainer.value = containerRef
      }
    })
  }
  
  // Carregar histórico
  const carregarHistorico = async () => {
    if (produto.value.id) {
      await carregarHistoricoCompleto(produto.value.id)
      if (produto.value.nome && produto.value.concorrente) {
        atualizarTituloGrafico(produto.value.nome, produto.value.concorrente)
      }
    }
  }
  
  // Lifecycle hooks
  onMounted(() => {
    carregarProduto()
    window.addEventListener('resize', resizeChart)
  })
  
  onUnmounted(() => {
    window.removeEventListener('resize', resizeChart)
  })
  
  // Watch para recarregar produto
  watch(() => produto.value.id, async (newId) => {
    if (newId) {
      conectarRefsGrafico()
      await carregarHistorico()
    }
  })
  
  // Watch para quando o produto for carregado 
  watch(() => produto.value.id, () => {
    if (produto.value.id) {
      nextTick(() => {
        conectarRefsGrafico()
        carregarHistorico()
      })
    }
  }, { immediate: true })
  </script>
  
  <style scoped>
  .detail-card {
    border-radius: 8px;
    overflow: hidden;
    transition: all 0.3s ease;
  }
  
  .detail-card:hover {
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
  }
  </style>