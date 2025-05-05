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
        <!-- Debug info -->
        <v-alert v-if="debugInfo" type="info" class="mb-4">
          {{ debugInfo }}
        </v-alert>
        
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
    debugInfo
  } = usePriceHistory()
  
  // Referência para o componente de gráfico
  const priceChartComponent = ref(null)
  
  // Conectar refs do gráfico
  const conectarRefsGrafico = () => {
    nextTick(() => {
      if (priceChartComponent.value) {
        // Obter as refs expostas pelo componente
        const exposedRefs = priceChartComponent.value
        
        if (exposedRefs) {
          priceChart.value = exposedRefs.priceChart
          chartContainer.value = exposedRefs.chartContainer
          
          debugInfo.value = 'Refs conectadas: ' + 
            (priceChart.value ? 'Canvas OK' : 'Canvas NULL') + ', ' +
            (chartContainer.value ? 'Container OK' : 'Container NULL')
          
          // Verificar dimensões do container
          if (exposedRefs.checkDimensions) {
            exposedRefs.checkDimensions()
          }
        }
      }
    })
  }
  
  // Carregar histórico
  const carregarHistorico = async () => {
    if (produto.value.id) {
      debugInfo.value = `Carregando histórico para produto ID: ${produto.value.id}`
      await carregarHistoricoCompleto(produto.value.id)
      
      if (produto.value.nome && produto.value.concorrente) {
        atualizarTituloGrafico(produto.value.nome, produto.value.concorrente)
      }
    } else {
      debugInfo.value = 'Produto sem ID para carregar histórico'
    }
  }
  
  // Lifecycle hooks
  onMounted(() => {
    carregarProduto()
  })
  
  // Watch para produto carregado
  watch(() => produto.value.id, (newId) => {
    if (newId) {
      conectarRefsGrafico()
      
      // Carregar histórico após garantir que as refs estão conectadas
      nextTick(() => {
        carregarHistorico()
      })
    }
  }, { immediate: true })
  
  // Watch adicional para garantir que as refs sejam conectadas quando o componente estiver disponível
  watch(() => priceChartComponent.value, (newRef) => {
    if (newRef) {
      conectarRefsGrafico()
    }
  })
  </script>