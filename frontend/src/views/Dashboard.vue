# frontend/src/views/Dashboard.vue (Refatorado)

```vue
<template>
  <v-container fluid>
    <!-- Cabeçalho da página -->
    <dashboard-header
      title="Dashboard"
      subtitle="Monitore seus produtos e concorrentes"
      @add-product="$router.push('/products/add')"
    />
    
    <!-- Cards de informações -->
    <dashboard-stats :stats="stats" />
    
    <!-- Botão para abrir o modal do gráfico comparativo -->
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4" elevation="2">
          <v-card-text class="d-flex align-center pa-4">
            <v-icon color="primary" size="32" class="mr-4">mdi-chart-line</v-icon>
            <div>
              <div class="text-h6 mb-1">Análise Comparativa de Preços</div>
              <div class="text-body-2 text-grey">Visualize a evolução de preços de todos os produtos ao longo do tempo</div>
            </div>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              @click="abrirGraficoComparativo(produtos)"
              :loading="carregandoHistoricoComparativo"
            >
              <v-icon left>mdi-chart-line</v-icon>
              Ver Gráfico Comparativo
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Conteúdo principal -->
    <v-card class="rounded-lg" elevation="3">
      <v-toolbar flat class="primary lighten-1" dark>
        <v-toolbar-title>
          <v-icon left>mdi-compare-horizontal</v-icon>
          Comparação de Produtos
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Pesquisar produto"
          hide-details
          dense
          class="mt-2 mr-4"
          style="max-width: 300px;"
          outlined
          dark
          color="white"
          single-line
        ></v-text-field>
        <v-btn
          icon
          :loading="loading"
          @click="carregarDados"
          color="white"
          class="ml-2"
        >
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </v-toolbar>
      
      <!-- Estado de carregamento -->
      <v-progress-linear
        indeterminate
        v-if="loading"
        color="primary"
      ></v-progress-linear>
      
      <!-- Conteúdo da tabela -->
      <v-card-text class="pa-4">
        <!-- Estado vazio quando não há produtos -->
        <empty-state
          v-if="produtosAgrupados.length === 0 && !loading"
          @action="$router.push('/products/add')"
        />
        
        <!-- Lista de grupos de produtos filtrados -->
        <div v-if="produtosAgrupadosFiltrados.length > 0">
          <product-group-card
            v-for="(grupo, index) in produtosAgrupadosFiltrados"
            :key="index"
            :grupo="grupo"
            :get-preco="getPreco"
            :verificando-item="verificandoItem"
            :is-open="gruposAbertos.includes(index)"
            @toggle="toggleGrupo(index)"
            @open-chart="abrirGraficoGrupo"
            @view-details="verDetalhes"
            @verify-price="verificarPreco"
            @set-base="definirProdutoClienteBase"
            @delete="excluirProduto"
          />
        </div>

        <!-- Mensagem quando o filtro não encontrar resultados -->
        <empty-state
          v-if="produtosAgrupados.length > 0 && produtosAgrupadosFiltrados.length === 0"
          title="Nenhum produto corresponde à sua pesquisa"
          :show-button="false"
        />
      </v-card-text>
    </v-card>
    
    <!-- Modal para o gráfico comparativo -->
    <comparative-chart-modal
      :mostrar-grafico-comparativo="mostrarGraficoComparativo"
      :carregando-historico-comparativo="carregandoHistoricoComparativo"
      :dados-historico-comparativo="dadosHistoricoComparativo"
      :grupo-selecionado="grupoSelecionado"
      :filtro-grafico="filtroGrafico"
      :tipos-produto-filtro="tiposProdutoFiltro"
      :periodos-filtro="periodosFiltro"
      :produtos-para-filtro="produtosParaFiltro"
      @fechar="fecharGraficoComparativo"
      @filtro-changed="onFiltroChanged"
      @atualizar="atualizarGraficoComparativo"
      ref="chartModal"
    />
    
    <!-- Snackbar para mensagens -->
    <custom-snackbar />
  </v-container>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useProducts } from '@/composables/useProducts'
import { useProductFilter } from '@/composables/useProductFilter'
import { usePriceChart } from '@/composables/usePriceChart'
import { useSnackbar } from '@/composables/useSnackbar'

import DashboardHeader from '@/components/dashboard/DashboardHeader.vue'
import DashboardStats from '@/components/dashboard/DashboardStats.vue'
import ProductGroupCard from '@/components/dashboard/ProductGroupCard.vue'
import ComparativeChartModal from '@/components/dashboard/ComparativeChartModal.vue'
import EmptyState from '@/components/dashboard/EmptyState.vue'
import CustomSnackbar from '@/components/common/CustomSnackbar.vue'

const router = useRouter()

// Composables
const {
  loading,
  produtos,
  verificandoItem,
  carregarDados,
  verificarPreco,
  definirProdutoClienteBase,
  excluirProduto,
  getPreco
} = useProducts()

const {
  search,
  gruposAbertos,
  produtosUnicos,
  concorrentesUnicos,
  produtosAgrupados,
  produtosAgrupadosFiltrados,
  toggleGrupo
} = useProductFilter(produtos)

const {
  mostrarGraficoComparativo,
  carregandoHistoricoComparativo,
  chartComparativo,
  chartContainerComparativo,
  grupoSelecionado,
  dadosHistoricoComparativo,
  tiposProdutoFiltro,
  periodosFiltro,
  filtroGrafico,
  abrirGraficoGrupo,
  abrirGraficoComparativo,
  fecharGraficoComparativo,
  atualizarGraficoComparativo,
  onFiltroChanged,
  carregarHistoricoComparativo,
  getProdutosParaFiltro
} = usePriceChart()

const { mostrarSnackbar } = useSnackbar()

// Ref para o modal do gráfico
const chartModal = ref(null)

// Stats para o dashboard
const stats = computed(() => ({
  totalProdutos: produtosUnicos.value.length,
  totalConcorrentes: concorrentesUnicos.value.length,
  totalComparacoes: produtos.value.length
}))

// Produtos para o filtro do gráfico
const produtosParaFiltro = computed(() => {
  return getProdutosParaFiltro(produtos.value)
})

// Navegar para detalhes do produto
const verDetalhes = (produtoId) => {
  if (produtoId) {
    router.push(`/products/${produtoId}`)
  }
}

// Handler para verificar preço
const handleVerificarPreco = async (produtoId) => {
  try {
    await verificarPreco(produtoId)
    mostrarSnackbar('Preço verificado com sucesso')
  } catch (error) {
    mostrarSnackbar('Erro ao verificar preço', 'error')
  }
}

// Handler para definir produto cliente base
const handleDefinirProdutoClienteBase = async (produto) => {
  try {
    await definirProdutoClienteBase(produto)
    mostrarSnackbar('Produto definido como base para comparações')
  } catch (error) {
    mostrarSnackbar(error.message || 'Erro ao definir produto cliente base', 'error')
  }
}

// Handler para excluir produto
const handleExcluirProduto = async (produto) => {
  if (!confirm(`Tem certeza que deseja excluir o produto "${produto.nome}"?`)) {
    return
  }
  
  try {
    await excluirProduto(produto)
    mostrarSnackbar('Produto excluído com sucesso', 'success')
  } catch (error) {
    mostrarSnackbar(error.message || 'Erro ao excluir produto', 'error')
  }
}

// Configurar referências do gráfico quando o modal for aberto
const setupChartRefs = () => {
  if (chartModal.value) {
    nextTick(() => {
      // Atualizar as referências para o componente de gráfico
      const { chart, chartContainer } = chartModal.value
      chartComparativo.value = chart
      chartContainerComparativo.value = chartContainer
    })
  }
}

// Função para ajustar o gráfico quando a janela mudar de tamanho
const resizeHandler = () => {
  if (chartModal.value?.chartInstance) {
    chartModal.value.chartInstance.resize()
  }
}

// Lifecycle hooks
onMounted(() => {
  carregarDados()
  
  // Abrir o primeiro grupo
  nextTick(() => {
    if (produtosAgrupados.value.length > 0 && gruposAbertos.value.length === 0) {
      gruposAbertos.value.push(0)
    }
  })
  
  window.addEventListener('resize', resizeHandler)
  setupChartRefs()
})

onUnmounted(() => {
  window.removeEventListener('resize', resizeHandler)
})
</script>

<style scoped>
/* Estilos específicos do dashboard podem ser mantidos aqui se necessário */
</style>
```