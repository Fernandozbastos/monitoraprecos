<template>
  <v-container fluid>
    <!-- Cabeçalho da página com visual aprimorado -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="2" class="mb-6 gradient-header">
          <v-card-text>
            <div class="d-flex flex-wrap align-center">
              <div>
                <h1 class="text-h4 font-weight-bold white--text mb-1">Dashboard</h1>
                <p class="text-subtitle-1 white--text mb-0">Monitore seus produtos e concorrentes</p>
              </div>
              <v-spacer></v-spacer>
              <v-btn
                color="white"
                class="primary--text text-none px-4 elevation-1"
                @click="$router.push('/products/add')"
              >
                <v-icon left>mdi-plus</v-icon>
                Adicionar Produto
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Cards de informações com visual aprimorado -->
    <v-row>
      <v-col cols="12" md="4">
        <v-card class="mb-4 stats-card" elevation="3" rounded="lg">
          <v-card-text class="pa-4">
            <div class="d-flex align-center">
              <div class="rounded-circle primary pa-4 mr-4">
                <v-icon color="white" size="32">mdi-package-variant-closed</v-icon>
              </div>
              <div>
                <div class="text-overline text-grey">Total de Produtos</div>
                <div class="text-h4 font-weight-bold">{{ produtosUnicos.length }}</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card class="mb-4 stats-card" elevation="3" rounded="lg">
          <v-card-text class="pa-4">
            <div class="d-flex align-center">
              <div class="rounded-circle info pa-4 mr-4">
                <v-icon color="white" size="32">mdi-account-group</v-icon>
              </div>
              <div>
                <div class="text-overline text-grey">Concorrentes</div>
                <div class="text-h4 font-weight-bold">{{ concorrentesUnicos.length }}</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card class="mb-4 stats-card" elevation="3" rounded="lg">
          <v-card-text class="pa-4">
            <div class="d-flex align-center">
              <div class="rounded-circle success pa-4 mr-4">
                <v-icon color="white" size="32">mdi-compare</v-icon>
              </div>
              <div>
                <div class="text-overline text-grey">Comparações</div>
                <div class="text-h4 font-weight-bold">{{ produtos.length }}</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
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
              @click="abrirGraficoComparativo"
              :loading="carregandoHistoricoComparativo"
            >
              <v-icon left>mdi-chart-line</v-icon>
              Ver Gráfico Comparativo
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Conteúdo principal com visual aprimorado -->
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
        <div v-if="produtosAgrupados.length === 0 && !loading" class="text-center pa-8">
          <v-img
            src="@/assets/empty-products.svg"
            max-width="200"
            class="mx-auto mb-4"
            alt="Nenhum produto encontrado"
          ></v-img>
          <h3 class="text-h5 grey--text text--darken-1 mt-4">Nenhum produto encontrado</h3>
          <p class="text-body-1 grey--text mb-6">Comece adicionando produtos usando o botão no topo da página</p>
          <v-btn
            color="primary"
            @click="$router.push('/products/add')"
          >
            <v-icon left>mdi-plus</v-icon>
            Adicionar Produto
          </v-btn>
        </div>
        
        <!-- Lista de grupos de produtos filtrados -->
        <div v-if="produtosAgrupadosFiltrados.length > 0">
          <div
            v-for="(grupo, index) in produtosAgrupadosFiltrados"
            :key="index"
            class="mb-5 produto-grupo"
          >
            <!-- Cabeçalho do grupo com visual aprimorado -->
            <div 
              class="d-flex align-center pa-4 grupo-header"
              @click="toggleGrupo(index)"
              :class="{'grupo-header-active': gruposAbertos.includes(index)}"
            >
              <v-icon class="mr-2 transition-swing" :class="{'transform-rotate-90': gruposAbertos.includes(index)}">
                mdi-chevron-right
              </v-icon>
              
              <!-- Nome do produto -->
              <span class="text-subtitle-1 font-weight-bold">{{ grupo.nome }}</span>
              
              <!-- Mensagem quando não houver produto cliente definido -->
              <v-chip
                v-if="!grupo.produtoClienteBase"
                small
                outlined
                color="warning"
                class="ml-3"
              >
                <v-icon left size="16">mdi-alert-circle</v-icon>
                Por favor, defina o produto cliente
              </v-chip>
              
              <v-spacer></v-spacer>
              
              <!-- Botão para ver histórico de preços deste grupo -->
              <v-btn
                small
                outlined
                color="primary"
                class="mr-2"
                @click.stop="abrirGraficoGrupo(grupo)"
              >
                <v-icon left small>mdi-chart-line</v-icon>
                Ver Histórico
              </v-btn>
              
              <!-- Resumo do produto (apenas se houver produto cliente base) -->
              <template v-if="grupo.produtoClienteBase">
                <div class="d-none d-md-flex align-center">
                  <!-- Preço do cliente -->
                  <div class="text-center mx-3 resumo-grupo">
                    <div class="caption grey--text">Preço Cliente</div>
                    <div class="subtitle-1 font-weight-medium primary--text">
                      {{ 
                        grupo.produtoClienteBase.preco_cliente ? 
                        formatarPreco(grupo.produtoClienteBase.preco_cliente) : 
                        'N/A' 
                      }}
                    </div>
                  </div>
                  
                  <!-- Menor preço concorrente -->
                  <div class="text-center mx-3 resumo-grupo">
                    <div class="caption grey--text">Menor Preço</div>
                    <div class="subtitle-1 font-weight-medium">
                      {{ 
                        grupo.menorPrecoConcorrente ? 
                        formatarPreco(grupo.menorPrecoConcorrente) : 
                        'N/A' 
                      }}
                    </div>
                  </div>
                  
                  <!-- Diferença percentual -->
                  <div class="text-center mx-3" v-if="grupo.diferencaPercentual !== null">
                    <div class="caption grey--text">Variação</div>
                    <v-chip
                      small
                      :color="getCorDiferenca(grupo.diferencaPercentual)"
                      dark
                    >
                      {{ formatarPercentual(grupo.diferencaPercentual) }}
                    </v-chip>
                  </div>
                  
                  <!-- Concorrente com menor preço -->
                  <div class="text-center mx-3" v-if="grupo.concorrenteMenorPreco">
                    <div class="caption grey--text">Concorrente</div>
                    <div class="subtitle-2 font-weight-regular text-truncate" style="max-width: 150px">
                      {{ grupo.concorrenteMenorPreco }}
                    </div>
                  </div>
                </div>
              </template>
            </div>
            
            <!-- Conteúdo do grupo (tabela de produtos) -->
            <div v-if="gruposAbertos.includes(index)" class="pa-4 grupo-content">
              <v-data-table
                :headers="headers"
                :items="grupo.produtos"
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
                    {{ getPreco(item) }}
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
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          icon
                          x-small
                          color="primary"
                          class="mr-1"
                          @click="verDetalhes(item.id)"
                          v-bind="attrs"
                          v-on="on"
                        >
                          <v-icon>mdi-eye</v-icon>
                        </v-btn>
                      </template>
                      <span>Ver detalhes</span>
                    </v-tooltip>
                    
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          icon
                          x-small
                          color="success"
                          @click="verificarPreco(item.id)"
                          :loading="verificandoItem === item.id"
                          v-bind="attrs"
                          v-on="on"
                        >
                          <v-icon>mdi-refresh</v-icon>
                        </v-btn>
                      </template>
                      <span>Verificar preço</span>
                    </v-tooltip>
                    
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          icon
                          x-small
                          color="warning"
                          class="ml-1"
                          @click="definirProdutoClienteBase(item)"
                          :disabled="item.produto_cliente"
                          v-bind="attrs"
                          v-on="on"
                        >
                          <v-icon>mdi-star</v-icon>
                        </v-btn>
                      </template>
                      <span>Definir como produto cliente base</span>
                    </v-tooltip>

                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          icon
                          x-small
                          color="error"
                          class="ml-1"
                          @click="excluirProduto(item)"
                          v-bind="attrs"
                          v-on="on"
                        >
                          <v-icon>mdi-delete</v-icon>
                        </v-btn>
                      </template>
                      <span>Excluir produto</span>
                    </v-tooltip>
                  </div>
                </template>
              </v-data-table>
            </div>
          </div>
        </div>

        <!-- Mensagem quando o filtro não encontrar resultados -->
        <div v-if="produtosAgrupados.length > 0 && produtosAgrupadosFiltrados.length === 0" class="text-center pa-6">
          <v-icon size="48" color="grey lighten-1">mdi-file-search-outline</v-icon>
          <h3 class="text-h6 grey--text text--darken-1 mt-3">Nenhum produto corresponde à sua pesquisa</h3>
        </div>
      </v-card-text>
    </v-card>
    
    <!-- Modal para o gráfico comparativo -->
    <v-dialog
      v-model="mostrarGraficoComparativo"
      max-width="1200px"
      persistent
    >
      <v-card>
        <v-card-title class="primary white--text">
          <span v-if="grupoSelecionado">
            Histórico de Preços - {{ grupoSelecionado.nome }}
          </span>
          <span v-else>
            Gráfico Comparativo de Preços
          </span>
          <v-spacer></v-spacer>
          <v-btn
            icon
            color="white"
            @click="fecharGraficoComparativo"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        
        <v-card-text class="pa-6">
          <!-- Opções de filtro para o gráfico -->
          <v-row>
            <v-col cols="12" sm="4">
              <v-select
                v-model="filtroGrafico.tipoProduto"
                :items="tiposProdutoFiltro"
                item-text="text"
                item-value="value"
                label="Tipo de Produtos"
                outlined
                dense
                hide-details
                class="mb-4"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="4">
              <v-select
                v-model="filtroGrafico.produtoId"
                :items="produtosParaFiltro"
                item-text="nome_completo"
                item-value="id"
                label="Produto"
                outlined
                dense
                hide-details
                class="mb-4"
                return-object
              ></v-select>
            </v-col>
            <v-col cols="12" sm="4">
              <v-select
                v-model="filtroGrafico.periodo"
                :items="periodosFiltro"
                item-text="text"
                item-value="value"
                label="Período"
                outlined
                dense
                hide-details
                class="mb-4"
              ></v-select>
            </v-col>
          </v-row>
          
          <!-- Conteúdo do gráfico -->
          <div v-if="carregandoHistoricoComparativo" class="d-flex justify-center align-center py-12">
            <v-progress-circular indeterminate size="64" color="primary"></v-progress-circular>
            <span class="ml-4 text-subtitle-1">Carregando dados de histórico...</span>
          </div>
          
          <div v-else-if="!dadosHistoricoComparativo.length" class="text-center py-12">
            <v-icon size="64" color="grey lighten-1">mdi-chart-timeline-variant</v-icon>
            <h3 class="text-h6 grey--text text--darken-1 mt-4">Nenhum dado histórico encontrado</h3>
            <p class="text-body-2 grey--text mb-4">Selecione um produto ou verifique os preços para gerar dados históricos</p>
          </div>
          
          <div v-else ref="chartContainerComparativo" style="height: 500px; width: 100%;">
            <canvas ref="chartComparativo"></canvas>
          </div>
        </v-card-text>
        
        <v-card-actions class="pa-4">
          <v-btn
            text
            color="grey darken-1"
            @click="fecharGraficoComparativo"
          >
            Fechar
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            @click="atualizarGraficoComparativo"
            :loading="carregandoHistoricoComparativo"
          >
            <v-icon left>mdi-refresh</v-icon>
            Atualizar Gráfico
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Snackbar para mensagens -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
      bottom
      right
    >
      {{ snackbar.text }}
      <template v-slot:action="{ attrs }">
        <v-btn
          text
          v-bind="attrs"
          @click="snackbar.show = false"
        >
          Fechar
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import api from '@/services/api'
import Chart from 'chart.js/auto'

const router = useRouter()
const store = useStore()
const loading = ref(false)
const produtos = ref([])
const debug = ref(false)
const verificandoItem = ref(null)
const gruposAbertos = ref([])
const search = ref('') // Campo de pesquisa

// Variáveis para o gráfico comparativo
const mostrarGraficoComparativo = ref(false)
const carregandoHistoricoComparativo = ref(false)
const chartComparativo = ref(null)
const chartInstanceComparativo = ref(null)
const chartContainerComparativo = ref(null)
const dadosHistoricoComparativo = ref([])
const grupoSelecionado = ref(null)
const datasetsGrafico = ref([])

// Filtros para o gráfico
const filtroGrafico = ref({
  tipoProduto: 'todos',
  produtoId: null,  // Objeto único, não array
  periodo: '30'
})

// Opções para os filtros
const tiposProdutoFiltro = [
  { text: 'Todos os produtos', value: 'todos' },
  { text: 'Produtos do Cliente', value: 'cliente' },
  { text: 'Produtos de Concorrentes', value: 'concorrente' }
]

const periodosFiltro = [
  { text: 'Últimos 30 dias', value: '30' },
  { text: 'Últimos 60 dias', value: '60' },
  { text: 'Últimos 90 dias', value: '90' },
  { text: 'Tudo', value: 'all' }
]

// Produtos formatados para o filtro
const produtosParaFiltro = computed(() => {
  return produtos.value.map(p => ({
    id: p.id,
    nome_completo: `${p.nome} (${p.concorrente})`,
    nome: p.nome,
    concorrente: p.concorrente,
    tipo_produto: p.tipo_produto
  }))
})

// Estado para snackbar
const snackbar = ref({
  show: false,
  text: '',
  color: 'success',
  timeout: 3000
})

// Função para alternar a exibição de um grupo
const toggleGrupo = (index) => {
  const currentIndex = gruposAbertos.value.indexOf(index)
  if (currentIndex === -1) {
    gruposAbertos.value.push(index)
  } else {
    gruposAbertos.value.splice(currentIndex, 1)
  }
}

// Cabeçalhos da tabela
const headers = [
  { text: 'Tipo', value: 'tipo_produto', width: '100px' },
  { text: 'Base', value: 'produto_cliente', width: '80px', align: 'center' },
  { text: 'Empresa', value: 'concorrente' },
  { text: 'Preço', value: 'preco', width: '120px' },
  { text: 'Diferença', value: 'diferenca_percentual', width: '120px' },
  { text: 'Última Verificação', value: 'ultima_verificacao', width: '180px' },
  { text: 'Ações', value: 'actions', align: 'center', sortable: false, width: '140px' }
]

// Produtos únicos (pelo nome)
const produtosUnicos = computed(() => {
  const nomes = new Set()
  const unicos = []
  
  produtos.value.forEach(produto => {
    if (!nomes.has(produto.nome)) {
      nomes.add(produto.nome)
      unicos.push(produto)
    }
  })
  
  return unicos
})

// Concorrentes únicos
const concorrentesUnicos = computed(() => {
  const nomes = new Set()
  produtos.value.forEach(p => {
    if (p.tipo_produto === 'concorrente' && p.concorrente) {
      nomes.add(p.concorrente)
    }
  })
  return Array.from(nomes)
})

// Produtos agrupados por nome
const produtosAgrupados = computed(() => {
  const grupos = []
  const nomesProdutos = new Set()
  
  // Coletar nomes únicos
  produtos.value.forEach(p => nomesProdutos.add(p.nome))
  
  // Para cada nome, criar um grupo
  Array.from(nomesProdutos).forEach(nome => {
    const produtosDesseTipo = produtos.value.filter(p => p.nome === nome)
    
    // Produto cliente base (marcado como produto_cliente)
    const produtoClienteBase = produtosDesseTipo.find(p => p.produto_cliente === true)
    
    // Produtos concorrentes
    const produtosConcorrentes = produtosDesseTipo.filter(p => p.tipo_produto === 'concorrente')
    
    // Encontrar menor preço entre concorrentes
    let menorPrecoConcorrente = null
    let concorrenteMenorPreco = null
    
    if (produtosConcorrentes.length > 0) {
      // Filtrar produtos concorrentes com preços válidos
      const concorrentesComPreco = produtosConcorrentes.filter(p => {
        const preco = p.preco_ultimo || p.menor_preco_concorrente
        return preco !== null && preco !== undefined && !isNaN(preco) && preco > 0
      })
      
      if (concorrentesComPreco.length > 0) {
        // Encontrar o com menor preço
        let menorPreco = Number.MAX_SAFE_INTEGER
        let produtoMenorPreco = null
        
        concorrentesComPreco.forEach(p => {
          const preco = p.preco_ultimo || p.menor_preco_concorrente
          if (preco < menorPreco) {
            menorPreco = preco
            produtoMenorPreco = p
          }
        })
        
        menorPrecoConcorrente = menorPreco
        concorrenteMenorPreco = produtoMenorPreco?.concorrente
      }
    }
    
    // Se não tiver produto cliente base, usar qualquer produto do cliente
    let produtoClienteExibicao = produtoClienteBase
    if (!produtoClienteExibicao) {
      produtoClienteExibicao = produtosDesseTipo.find(p => p.tipo_produto === 'cliente')
    }
    
    // Calcular diferença percentual
    let diferencaPercentual = null
    if (produtoClienteExibicao && 
        produtoClienteExibicao.preco_cliente && 
        !isNaN(produtoClienteExibicao.preco_cliente) && 
        menorPrecoConcorrente && 
        !isNaN(menorPrecoConcorrente)) {
      
      diferencaPercentual = ((produtoClienteExibicao.preco_cliente - menorPrecoConcorrente) / menorPrecoConcorrente) * 100
      diferencaPercentual = Math.round(diferencaPercentual * 10) / 10
    }
    
    // Processar cada produto para exibição na tabela
    const produtosProcessados = produtosDesseTipo.map(p => {
      let diferencaIndividual = null
      
      // Para produtos do cliente, calcular a diferença em relação ao menor preço concorrente
      if (p.tipo_produto === 'cliente' && p.preco_cliente && menorPrecoConcorrente) {
        diferencaIndividual = ((p.preco_cliente - menorPrecoConcorrente) / menorPrecoConcorrente) * 100
        diferencaIndividual = Math.round(diferencaIndividual * 10) / 10
      }
      
      // Para produtos concorrentes, calcular a diferença em relação ao produto cliente base
      if (p.tipo_produto === 'concorrente' && produtoClienteExibicao && produtoClienteExibicao.preco_cliente) {
        const precoConcorrente = p.preco_ultimo || p.menor_preco_concorrente
        if (precoConcorrente) {
          diferencaIndividual = ((precoConcorrente - produtoClienteExibicao.preco_cliente) / produtoClienteExibicao.preco_cliente) * 100
          diferencaIndividual = Math.round(diferencaIndividual * 10) / 10
        }
      }
      
      return {
        ...p,
        preco_exibicao: p.tipo_produto === 'cliente' 
          ? p.preco_cliente 
          : (p.preco_ultimo || p.menor_preco_concorrente),
        diferenca_percentual: diferencaIndividual
      }
    })
    
    grupos.push({
      nome,
      produtos: produtosProcessados,
      produtoClienteBase: produtoClienteExibicao,
      menorPrecoConcorrente,
      concorrenteMenorPreco,
      diferencaPercentual
    })
  })
  
  // Ordenar grupos pela presença de um produto cliente base primeiro
  return grupos.sort((a, b) => {
    // Priorizar grupos com produto cliente base
    if (a.produtoClienteBase && !b.produtoClienteBase) return -1
    if (!a.produtoClienteBase && b.produtoClienteBase) return 1
    // Em seguida, ordenar alfabeticamente pelo nome
    return a.nome.localeCompare(b.nome)
  })
})

// Produtos filtrados com base na pesquisa
const produtosAgrupadosFiltrados = computed(() => {
  if (!search.value) return produtosAgrupados.value
  
  const searchTerm = search.value.toLowerCase().trim()
  
  return produtosAgrupados.value.filter(grupo => {
    // Verifica se o nome do grupo contém o termo de pesquisa
    if (grupo.nome.toLowerCase().includes(searchTerm)) return true
    
    // Verifica se algum produto deste grupo contém o termo de pesquisa
    return grupo.produtos.some(produto => 
      produto.nome.toLowerCase().includes(searchTerm) || 
      produto.concorrente.toLowerCase().includes(searchTerm)
    )
  })
})

// Exibir mensagem no snackbar
const mostrarSnackbar = (texto, cor = 'success', timeout = 3000) => {
  snackbar.value = {
    show: true,
    text: texto,
    color: cor,
    timeout: timeout
  }
}

// Função para definir um produto como cliente base
const definirProdutoClienteBase = async (produto) => {
  try {
    // Verificar se existe um cliente atual selecionado
    if (!store.getters['auth/user']?.cliente_atual) {
      mostrarSnackbar('Por favor, selecione um cliente atual no menu superior antes de continuar', 'warning');
      return;
    }
    
    // Obter o ID do cliente atual
    const clienteId = typeof store.getters['auth/user'].cliente_atual === 'object' 
      ? store.getters['auth/user'].cliente_atual.id 
      : store.getters['auth/user'].cliente_atual;
    
    // Obter o grupo do produto
    const grupoId = typeof produto.grupo === 'object' 
      ? produto.grupo.id 
      : produto.grupo;
    
    // 1. Primeiro, encontrar TODOS os produtos com o mesmo nome que não são o atual
    const outrosProdutos = produtos.value.filter(p => 
      p.nome === produto.nome && 
      p.id !== produto.id
    );
    
    // 2. Se houver algum produto que está marcado como produto_cliente, desmarcá-lo
    const produtosMarcadosComoBase = outrosProdutos.filter(p => p.produto_cliente === true);
    
    if (produtosMarcadosComoBase.length > 0) {
      for (const produtoAnterior of produtosMarcadosComoBase) {
        try {
          await api.patch(`/produtos/${produtoAnterior.id}/`, {
            produto_cliente: false,
            tipo_produto: 'concorrente', // Mudar para concorrente
            cliente: clienteId,
            grupo: grupoId
          });
          
          // Atualizar localmente
          const idx = produtos.value.findIndex(p => p.id === produtoAnterior.id);
          if (idx !== -1) {
            produtos.value[idx].produto_cliente = false;
            produtos.value[idx].tipo_produto = 'concorrente';
          }
        } catch (err) {
          console.error(`Erro ao desmarcar produto ${produtoAnterior.id}:`, err);
        }
      }
    }
    
    // 3. Agora, garantir que TODOS os outros produtos com o mesmo nome sejam marcados como concorrentes
    for (const outroProduto of outrosProdutos) {
      // Se ainda não for marcado como concorrente, marcá-lo
      if (outroProduto.tipo_produto !== 'concorrente') {
        try {
          await api.patch(`/produtos/${outroProduto.id}/`, {
            tipo_produto: 'concorrente',
            produto_cliente: false, // Garantir que não seja cliente base
            cliente: clienteId,
            grupo: grupoId
          });
          
          // Atualizar localmente
          const idx = produtos.value.findIndex(p => p.id === outroProduto.id);
          if (idx !== -1) {
            produtos.value[idx].tipo_produto = 'concorrente';
            produtos.value[idx].produto_cliente = false;
          }
        } catch (err) {
          console.error(`Erro ao alterar tipo do produto ${outroProduto.id}:`, err);
        }
      }
    }
    
    // 4. Finalmente, atualizar o produto selecionado como cliente base
    const dadosAtualizacao = {
      produto_cliente: true,
      tipo_produto: 'cliente', // Garantir que seja do tipo cliente
      cliente: clienteId,
      grupo: grupoId,
    };
    
    // Atualizar o produto com o novo status
    await api.patch(`/produtos/${produto.id}/`, dadosAtualizacao);
    
    // Atualizar localmente o produto antes de recarregar tudo
    const produtoIndex = produtos.value.findIndex(p => p.id === produto.id);
    if (produtoIndex !== -1) {
      produtos.value[produtoIndex].produto_cliente = true;
      produtos.value[produtoIndex].tipo_produto = 'cliente';
    }
    
    // Recarregar dados após a atualização
    await carregarDados();
    
    mostrarSnackbar('Produto definido como base para comparações');
    
  } catch (error) {
    console.error('Erro ao definir produto cliente base:', error);
    
    if (error.response) {
      if (error.response.status === 400) {
        let mensagemErro = '';
        if (typeof error.response.data === 'object') {
          for (const campo in error.response.data) {
            mensagemErro += `${campo}: ${error.response.data[campo].join(', ')}. `;
          }
        } else {
          mensagemErro = error.response.data.detail || 'Erro na validação dos dados.';
        }
        mostrarSnackbar(`Erro: ${mensagemErro}`, 'error');
      } 
      else if (error.response.status === 403) {
        mostrarSnackbar('Este produto não pertence ao cliente atual selecionado.', 'error');
      }
      else {
        mostrarSnackbar(`Erro ao definir produto cliente base: ${error.response.data.detail || 'Erro interno do servidor'}`, 'error');
      }
    } else {
      mostrarSnackbar('Erro de conexão ao tentar atualizar o produto', 'error');
    }
  }
}

// Função para obter o preço do produto (cliente ou concorrente)
const getPreco = (produto) => {
  // Para produtos do cliente
  if (produto.tipo_produto === 'cliente') {
    // Verificar se preco_cliente existe e é válido
    if (produto.preco_cliente !== null && produto.preco_cliente !== undefined && 
        !isNaN(produto.preco_cliente) && produto.preco_cliente > 0) {
      return formatarPreco(produto.preco_cliente);
    }
    
    // Caso não tenha, verificar preco_ultimo
    if (produto.preco_ultimo !== null && produto.preco_ultimo !== undefined && 
        !isNaN(produto.preco_ultimo) && produto.preco_ultimo > 0) {
      return formatarPreco(produto.preco_ultimo);
    }
    
    // Se não tiver nenhum, mostrar placeholder
    return 'Preço não definido';
  } 
  // Para produtos concorrentes
  else {
    // Verificar preco_ultimo (do histórico)
    if (produto.preco_ultimo !== null && produto.preco_ultimo !== undefined && 
        !isNaN(produto.preco_ultimo) && produto.preco_ultimo > 0) {
      return formatarPreco(produto.preco_ultimo);
    }
    
    // Verificar menor_preco_concorrente
    if (produto.menor_preco_concorrente !== null && produto.menor_preco_concorrente !== undefined && 
        !isNaN(produto.menor_preco_concorrente) && produto.menor_preco_concorrente > 0) {
      return formatarPreco(produto.menor_preco_concorrente);
    }
    
    // Se não tiver nenhum, mostrar placeholder
    return 'Preço não verificado';
  }
}

// Formatação de preço
const formatarPreco = (valor) => {
  if (valor === null || valor === undefined || isNaN(valor)) {
    return 'N/A';
  }
  
  // Garantir que seja tratado como número
  const numero = Number(valor);
  if (isNaN(numero)) {
    return 'N/A';
  }
  
  return `R$ ${numero.toFixed(2).replace('.', ',')}`;
}

// Formatação de percentual
const formatarPercentual = (valor) => {
  if (valor === null || valor === undefined || isNaN(valor)) {
    return 'N/A';
  }
  
  // Garantir que seja tratado como número
  const numero = Number(valor);
  if (isNaN(numero)) {
    return 'N/A';
  }
  
  const sinal = numero > 0 ? '+' : '';
  return `${sinal}${numero.toFixed(1).replace('.', ',')}%`;
}

// Determinar a cor da diferença
const getCorDiferenca = (diferenca) => {
  if (diferenca === null || diferenca === undefined || isNaN(diferenca)) return 'grey'
  return diferenca <= 0 ? 'success' : 'error'
}

// Formatar data
const formatDate = (dateString) => {
  if (!dateString) return 'Nunca verificado'
  try {
    const options = { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }
    return new Date(dateString).toLocaleString('pt-BR', options)
  } catch (error) {
    console.error('Erro ao formatar data:', error)
    return dateString || '-'
  }
}

// Formatação de data mais simples para o gráfico
const formatDateShort = (dateString) => {
  if (!dateString) return '';
  const options = { day: '2-digit', month: '2-digit', year: '2-digit' };
  try {
    return new Date(dateString).toLocaleString('pt-BR', options);
  } catch (e) {
    console.error('Erro ao formatar data curta:', e);
    return dateString;
  }
}

// Função para abrir o modal do gráfico para um grupo específico
const abrirGraficoGrupo = (grupo) => {
  grupoSelecionado.value = grupo;
  
  // Selecionar o primeiro produto deste grupo para o filtro
  if (grupo.produtos.length > 0) {
    const primeiroProduto = produtosParaFiltro.value.find(p => p.id === grupo.produtos[0].id);
    filtroGrafico.value.produtoId = primeiroProduto || null;
  }
  
  // Abrir o modal
  mostrarGraficoComparativo.value = true;
  
  // Carregar dados do histórico para este produto
  carregarHistoricoComparativo();
}

// Função para abrir o modal do gráfico geral
const abrirGraficoComparativo = () => {
  grupoSelecionado.value = null;
  mostrarGraficoComparativo.value = true;
  
  // Se não tiver produto selecionado, selecionar o primeiro por padrão
  if (!filtroGrafico.value.produtoId && produtosParaFiltro.value.length > 0) {
    filtroGrafico.value.produtoId = produtosParaFiltro.value[0];
  }
  
  // Carregar dados do histórico
  carregarHistoricoComparativo();
}

// Fechar o modal do gráfico
const fecharGraficoComparativo = () => {
  grupoSelecionado.value = null;
  mostrarGraficoComparativo.value = false;
  
  // Destruir o gráfico para liberar recursos
  if (chartInstanceComparativo.value) {
    chartInstanceComparativo.value.destroy();
    chartInstanceComparativo.value = null;
  }
}

// Atualizar o gráfico com base nos filtros
const atualizarGraficoComparativo = () => {
  carregarHistoricoComparativo();
}

// Carregar histórico de preços para o gráfico comparativo
const carregarHistoricoComparativo = async () => {
  if (!filtroGrafico.value.produtoId) {
    dadosHistoricoComparativo.value = [];
    mostrarSnackbar('Selecione um produto para visualizar o histórico', 'warning');
    return;
  }
  
  carregandoHistoricoComparativo.value = true;
  
  try {
    // Dados para armazenar o histórico
    const todosHistoricos = [];
    
    // Obter o ID do produto selecionado
    const produtoId = filtroGrafico.value.produtoId.id;
    
    // Informações do produto
    const produtoInfo = produtos.value.find(p => p.id === produtoId);
    
    if (!produtoInfo) {
      dadosHistoricoComparativo.value = [];
      return;
    }
    
    // Filtrar por tipo de produto, se necessário
    if (filtroGrafico.value.tipoProduto !== 'todos' && produtoInfo.tipo_produto !== filtroGrafico.value.tipoProduto) {
      dadosHistoricoComparativo.value = [];
      return;
    }
    
    // Carregar o histórico de preços
    const historicoResponse = await api.get(`/produtos/${produtoId}/historico/?limit=100`);
    
    if (Array.isArray(historicoResponse.data) && historicoResponse.data.length > 0) {
      // Calcular a data limite com base no período selecionado
      const hoje = new Date();
      let dataLimite = null;
      
      if (filtroGrafico.value.periodo !== 'all') {
        const dias = parseInt(filtroGrafico.value.periodo);
        dataLimite = new Date();
        dataLimite.setDate(dataLimite.getDate() - dias);
      }
      
      // Filtrar os dados por período, se necessário
      let dadosFiltrados = [...historicoResponse.data];
      
      if (dataLimite) {
        dadosFiltrados = dadosFiltrados.filter(item => {
          const dataItem = new Date(item.data);
          return dataItem >= dataLimite;
        });
      }
      
      // Adicionar os dados ao histórico combinado
      if (dadosFiltrados.length > 0) {
        // Ordenar por data (do mais antigo para o mais recente)
        const dadosOrdenados = dadosFiltrados.sort(
          (a, b) => new Date(a.data) - new Date(b.data)
        );
        
        // Adicionar informações do produto para identificação no gráfico
        const historicoProcessado = {
          produtoId: produtoId,
          nome: produtoInfo.nome,
          concorrente: produtoInfo.concorrente,
          tipo_produto: produtoInfo.tipo_produto,
          dados: dadosOrdenados
        };
        
        todosHistoricos.push(historicoProcessado);
      }
    }
    
    // Atualizar os dados e renderizar o gráfico
    dadosHistoricoComparativo.value = todosHistoricos;
    
    // Se tiver dados, renderizar o gráfico
    if (todosHistoricos.length > 0) {
      nextTick(() => {
        renderizarGraficoComparativo();
      });
    }
    
  } catch (error) {
    console.error('Erro ao carregar histórico para o gráfico comparativo:', error);
    mostrarSnackbar('Erro ao carregar dados históricos', 'error');
  } finally {
    carregandoHistoricoComparativo.value = false;
  }
}

// Renderizar o gráfico comparativo
const renderizarGraficoComparativo = () => {
  if (chartInstanceComparativo.value) {
    chartInstanceComparativo.value.destroy();
  }
  
  if (!chartComparativo.value || dadosHistoricoComparativo.value.length === 0) return;
  
  const ctx = chartComparativo.value.getContext('2d');
  
  // Com apenas um produto, o gráfico é mais simples
  const historicoItem = dadosHistoricoComparativo.value[0];
  
  // Extrair datas e preços
  const datasOrdenadas = historicoItem.dados.map(item => item.data);
  const precos = historicoItem.dados.map(item => parseFloat(item.preco));
  
  // Criar o dataset
  const dataset = {
    label: `${historicoItem.nome} (${historicoItem.concorrente})`,
    data: precos,
    borderColor: historicoItem.tipo_produto === 'cliente' ? 'rgba(63, 81, 181, 1)' : 'rgba(255, 87, 34, 1)',
    backgroundColor: historicoItem.tipo_produto === 'cliente' ? 'rgba(63, 81, 181, 0.1)' : 'rgba(255, 87, 34, 0.1)',
    borderWidth: 3,
    pointRadius: 5,
    pointBackgroundColor: historicoItem.tipo_produto === 'cliente' ? 'rgba(63, 81, 181, 1)' : 'rgba(255, 87, 34, 1)',
    tension: 0.2,
    fill: true
  };
  
  // Configurar e criar o gráfico
  chartInstanceComparativo.value = new Chart(ctx, {
    type: 'line',
    data: {
      labels: datasOrdenadas.map(data => formatDateShort(data)),
      datasets: [dataset]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: false,
          title: {
            display: true,
            text: 'Preço (R$)'
          },
          ticks: {
            callback: function(value) {
              return 'R$ ' + value.toFixed(2);
            }
          }
        },
        x: {
          title: {
            display: true,
            text: 'Data'
          }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function(context) {
              const value = context.parsed.y;
              return `Preço: R$ ${value.toFixed(2)}`;
            }
          }
        },
        legend: {
          display: true,
          position: 'top'
        },
        title: {
          display: true,
          text: grupoSelecionado.value ? 
            `Histórico de Preços - ${grupoSelecionado.value.nome}` : 
            'Histórico de Preços',
          font: {
            size: 16
          }
        }
      },
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false
      },
      animation: {
        duration: 1000
      }
    }
  });
}

// Função para excluir um produto
const excluirProduto = async (produto) => {
  try {
    // Verificar se existe um cliente atual selecionado
    if (!store.getters['auth/user']?.cliente_atual) {
      mostrarSnackbar('Por favor, selecione um cliente atual no menu superior antes de continuar', 'warning');
      return;
    }
    
    // Solicitar confirmação do usuário
    if (!confirm(`Tem certeza que deseja excluir o produto "${produto.nome}"?`)) {
      return;
    }
    
    // Verificar se é um produto cliente base
    const ehProdutoClienteBase = produto.produto_cliente === true;
    
    // Excluir o produto
    await api.delete(`/produtos/${produto.id}/`);
    
    // Se era um produto cliente base, verificar se há outros produtos do mesmo nome
    if (ehProdutoClienteBase) {
      // Buscar outros produtos com o mesmo nome
      const outrosProdutos = produtos.value.filter(p => 
        p.nome === produto.nome && 
        p.id !== produto.id
      );
      
      if (outrosProdutos.length > 0) {
        // Se houver outros produtos, podemos opcionalmente selecionar um novo produto cliente base
        // No momento, vamos deixar sem produto cliente base, mas poderia ser implementado aqui
        console.log(`O produto cliente base foi excluído. Existem ${outrosProdutos.length} outros produtos com o mesmo nome.`);
      }
    }
    
    // Remover o produto da lista local
    const produtoIndex = produtos.value.findIndex(p => p.id === produto.id);
    if (produtoIndex !== -1) {
      produtos.value.splice(produtoIndex, 1);
    }
    
    // Recarregar dados após a exclusão
    await carregarDados();
    
    mostrarSnackbar('Produto excluído com sucesso', 'success');
    
  } catch (error) {
    console.error('Erro ao excluir produto:', error);
    
    if (error.response) {
      console.error('Detalhes do erro:', error.response.data);
      
      if (error.response.status === 403) {
        mostrarSnackbar('Você não tem permissão para excluir este produto.', 'error');
      }
      else {
        mostrarSnackbar(`Erro ao excluir produto: ${error.response.data.detail || 'Erro interno do servidor'}`, 'error');
      }
    } else {
      mostrarSnackbar('Erro de conexão ao tentar excluir o produto', 'error');
    }
  }
}

// Função para verificar preço de um produto
const verificarPreco = async (produtoId) => {
  verificandoItem.value = produtoId
  try {
    await api.post(`/produtos/${produtoId}/verificar/`)
    // Recarregar os dados após verificar o preço
    await carregarDados()
    mostrarSnackbar('Preço verificado com sucesso')
  } catch (error) {
    console.error('Erro ao verificar preço:', error)
    mostrarSnackbar('Erro ao verificar preço', 'error')
  } finally {
    verificandoItem.value = null
  }
}

// Navegar para detalhes do produto
const verDetalhes = (produtoId) => {
  if (produtoId) {
    router.push(`/products/${produtoId}`)
  }
}

// Função para carregar dados
const carregarDados = async () => {
  loading.value = true;
  try {
    // Limpar os dados atuais
    produtos.value = [];
    
    // Usar timestamp para evitar cache
    const timestamp = new Date().getTime();
    
    // Buscar produtos
    const produtosResponse = await api.get(`/produtos/?t=${timestamp}`);
    
    if (produtosResponse.data.results && Array.isArray(produtosResponse.data.results)) {
      produtos.value = produtosResponse.data.results;
      
      // Para cada produto, recuperar o histórico de preços
      const produtosPromises = produtos.value.map(async (produto) => {
        try {
          // Recuperar histórico usando o endpoint correto
          const historicoResponse = await api.get(`/historico/?produto=${produto.id}&limit=1`);
          
          // Verificar se há resultados e se eles estão no formato esperado
          if (historicoResponse.data && 
              historicoResponse.data.results && 
              historicoResponse.data.results.length > 0) {
            
            // Obter o preço do histórico mais recente
            const precoHistorico = parseFloat(historicoResponse.data.results[0].preco);
            
            // Atribuir ao produto
            produto.preco_ultimo = precoHistorico;
            
            // Para produtos do cliente sem preço, usar o do histórico
            if (produto.tipo_produto === 'cliente' && 
                (!produto.preco_cliente || produto.preco_cliente === 0)) {
              produto.preco_cliente = precoHistorico;
              
              // Atualizar no backend
              try {
                await api.patch(`/produtos/${produto.id}/`, {
                  preco_cliente: precoHistorico,
                  cliente: produto.cliente,
                  grupo: produto.grupo
                });
              } catch (err) {
                console.error(`Erro ao atualizar preço no backend:`, err);
              }
            }
          }
        } catch (error) {
          console.error(`Erro ao carregar histórico do produto ${produto.id}:`, error);
        }
      });
      
      // Aguardar todas as promessas
      await Promise.all(produtosPromises);
      
      // Abrir o primeiro grupo
      if (produtosAgrupados.value.length > 0 && gruposAbertos.value.length === 0) {
        gruposAbertos.value.push(0);
      }
    } else {
      produtos.value = [];
    }
  } catch (error) {
    console.error('Erro ao carregar dados:', error);
    mostrarSnackbar('Erro ao carregar dados', 'error');
  } finally {
    loading.value = false;
  }
}

// Montar o componente
onMounted(() => {
  carregarDados()
})

// Ajustar o gráfico quando a janela mudar de tamanho
window.addEventListener('resize', () => {
  if (chartInstanceComparativo.value) {
    chartInstanceComparativo.value.resize()
  }
})
</script>

<style scoped>
.gradient-header {
  background: linear-gradient(135deg, var(--v-primary-base) 0%, var(--v-primary-darken1) 100%);
  border-radius: 8px;
}

.stats-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
}

.produto-grupo {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.12);
  transition: box-shadow 0.3s ease;
}

.produto-grupo:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.grupo-header {
  background-color: #f5f5f5;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  transition: background-color 0.2s ease;
  cursor: pointer;
}

.grupo-header:hover {
  background-color: #eeeeee;
}

.grupo-header-active {
  background-color: #e3f2fd; /* Azul claro para destacar o grupo ativo */
}

.grupo-content {
  background-color: white;
}

.transform-rotate-90 {
  transform: rotate(90deg);
}

.resumo-grupo {
  position: relative;
}

.resumo-grupo::after {
  content: "";
  position: absolute;
  right: -18px;
  top: 50%;
  height: 30px;
  border-right: 1px solid rgba(0, 0, 0, 0.12);
  transform: translateY(-50%);
}

.resumo-grupo:last-child::after {
  display: none;
}

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

.rounded-circle {
  border-radius: 50% !important;
}
</style>