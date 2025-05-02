<template>
  <v-container fluid>
    <!-- Cabeçalho da página -->
    <v-row>
      <v-col cols="12">
        <div class="d-flex align-center mb-6">
          <h1 class="text-h4 font-weight-bold primary--text">Dashboard</h1>
          <v-spacer></v-spacer>
          <v-btn
            color="success"
            class="text-none px-4"
            elevation="2"
            prepend-icon="mdi-plus"
            @click="$router.push('/products/add')"
          >
            Adicionar Produto
          </v-btn>
        </div>
      </v-col>
    </v-row>
    
    <!-- Cards de informações -->
    <v-row>
      <v-col cols="12" md="4">
        <v-card class="mb-4" elevation="3" rounded="lg">
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
        <v-card class="mb-4" elevation="3" rounded="lg">
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
        <v-card class="mb-4" elevation="3" rounded="lg">
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
    
    <!-- Conteúdo principal -->
    <v-card class="rounded-lg" elevation="3">
      <v-toolbar flat class="primary lighten-1" dark>
        <v-toolbar-title>Comparação de Produtos</v-toolbar-title>
        <v-spacer></v-spacer>
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
      <v-card-text class="pa-0">
        <div v-if="produtosAgrupados.length === 0 && !loading" class="text-center pa-8">
          <v-icon size="64" color="grey lighten-1">mdi-package-variant</v-icon>
          <h3 class="text-h5 grey--text text--darken-1 mt-4">Nenhum produto encontrado</h3>
          <p class="text-body-1 grey--text mb-6">Comece adicionando produtos usando o botão no topo da página</p>
          <v-btn
            color="primary"
            @click="$router.push('/products/add')"
            prepend-icon="mdi-plus"
          >
            Adicionar Produto
          </v-btn>
        </div>
        
        <!-- Grupos de produtos -->
        <template v-else>
          <v-expansion-panels v-model="expandedPanels" multiple class="px-4 py-4">
            <v-expansion-panel
              v-for="(grupo, index) in produtosAgrupados"
              :key="index"
              elevation="0"
              class="mb-4 rounded-lg produto-panel"
            >
              <v-expansion-panel-header class="py-3">
                <div class="d-flex align-center">
                  <h3 class="text-h6 font-weight-bold">{{ grupo.nome }}</h3>
                  <v-chip
                    v-if="temProdutoCliente(grupo.produtos)"
                    small
                    color="primary"
                    class="ml-4"
                  >
                    Cliente
                  </v-chip>
                  <v-chip
                    small
                    color="grey lighten-1"
                    class="ml-2"
                  >
                    {{ grupo.produtos.length }} produto(s)
                  </v-chip>
                </div>
              </v-expansion-panel-header>
              
              <v-expansion-panel-content>
                <v-data-table
                  :headers="headers"
                  :items="grupo.produtos"
                  :items-per-page="5"
                  class="elevation-0"
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
                      {{ item.tipo_produto === 'cliente' ? 'Meu Cliente' : item.concorrente }}
                    </span>
                  </template>
                  
                  <!-- Preço -->
                  <template v-slot:item.preco="{ item }">
                    <span :class="{'primary--text font-weight-bold': item.tipo_produto === 'cliente'}">
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
                    <span v-else class="text-caption grey--text">Não disponível</span>
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
                            v-bind="attrs"
                            v-on="on"
                            @click="verDetalhes(item.id)"
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
                            v-bind="attrs"
                            v-on="on"
                            @click="verificarPreco(item.id)"
                            :loading="verificandoItem === item.id"
                          >
                            <v-icon>mdi-refresh</v-icon>
                          </v-btn>
                        </template>
                        <span>Verificar preço</span>
                      </v-tooltip>
                    </div>
                  </template>
                </v-data-table>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </template>
      </v-card-text>
    </v-card>
    
    <!-- Debug Info (escondido por padrão) -->
    <v-card v-if="debug" elevation="3" class="mt-4 rounded-lg">
      <v-card-title class="primary lighten-1 white--text">
        Informações de Debug
        <v-spacer></v-spacer>
        <v-btn icon color="white" @click="debug = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <p><strong>Total de produtos carregados:</strong> {{ produtos.length }}</p>
        <p><strong>Produtos únicos:</strong> {{ produtosUnicos.length }}</p>
        <p><strong>Concorrentes únicos:</strong> {{ concorrentesUnicos.length }}</p>
        <p><strong>Primeiro produto:</strong></p>
        <pre class="grey lighten-4 pa-2 rounded">{{ JSON.stringify(produtos[0] || {}, null, 2) }}</pre>
        <p><strong>Produtos agrupados:</strong></p>
        <pre class="grey lighten-4 pa-2 rounded">{{ JSON.stringify(produtosAgrupados.slice(0, 1), null, 2) }}</pre>
      </v-card-text>
    </v-card>
    
    <!-- Botão de debug (discreto no canto inferior) -->
    <v-btn
      fab
      small
      color="grey lighten-3"
      class="debug-btn"
      @click="debug = !debug"
    >
      <v-icon color="grey darken-2">mdi-bug</v-icon>
    </v-btn>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()
const loading = ref(false)
const produtos = ref([])
const debug = ref(false)
const verificandoItem = ref(null)
const expandedPanels = ref([]) // Painéis expandidos por padrão

// Cabeçalhos da tabela
const headers = [
  { text: 'Tipo', value: 'tipo_produto', width: '120px' },
  { text: 'Empresa', value: 'concorrente' },
  { text: 'Preço', value: 'preco', width: '120px' },
  { text: 'Diferença', value: 'diferenca_percentual', width: '120px' },
  { text: 'Última Verificação', value: 'ultima_verificacao', width: '180px' },
  { text: 'Ações', value: 'actions', align: 'center', sortable: false, width: '100px' }
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
  
  // Primeiro, colete todos os nomes únicos de produtos
  produtos.value.forEach(p => nomesProdutos.add(p.nome))
  
  // Para cada nome de produto, crie um grupo
  Array.from(nomesProdutos).forEach(nome => {
    const produtosDesseTipo = produtos.value.filter(p => p.nome === nome)
    
    // Calcular o menor preço entre todos os produtos deste grupo
    let menorPreco = Number.MAX_SAFE_INTEGER
    
    produtosDesseTipo.forEach(p => {
      const preco = p.tipo_produto === 'cliente' ? p.preco_cliente : p.preco_ultimo || p.menor_preco_concorrente;
      if (preco && preco < menorPreco) {
        menorPreco = preco
      }
    })
    
    // Para cada produto no grupo, calcular a diferença percentual com o menor preço
    const produtosProcessados = produtosDesseTipo.map(p => {
      const preco = p.tipo_produto === 'cliente' ? p.preco_cliente : p.preco_ultimo || p.menor_preco_concorrente;
      let diferencaPercentual = null
      
      if (preco && menorPreco < Number.MAX_SAFE_INTEGER) {
        diferencaPercentual = ((preco - menorPreco) / menorPreco) * 100
      }
      
      return {
        ...p,
        diferenca_percentual: diferencaPercentual
      }
    })
    
    grupos.push({
      nome,
      produtos: produtosProcessados
    })
  })
  
  return grupos
})

// Verificar se o grupo tem um produto do cliente
const temProdutoCliente = (produtos) => {
  return produtos.some(p => p.tipo_produto === 'cliente')
}

// Montar o componente
onMounted(() => {
  carregarDados()
})

// Função para obter o preço do produto (cliente ou concorrente)
const getPreco = (produto) => {
  if (produto.tipo_produto === 'cliente') {
    return formatarPreco(produto.preco_cliente)
  } else {
    return formatarPreco(produto.preco_ultimo || produto.menor_preco_concorrente)
  }
}

// Formatar preço
const formatarPreco = (valor) => {
  if (valor === null || valor === undefined) return '-'
  return `R$ ${Number(valor).toFixed(2).replace('.', ',')}`
}

// Formatar percentual
const formatarPercentual = (valor) => {
  if (valor === null || valor === undefined) return '-'
  const sinal = valor > 0 ? '+' : ''
  return `${sinal}${valor.toFixed(1).replace('.', ',')}%`
}

// Determinar a cor da diferença
const getCorDiferenca = (diferenca) => {
  if (diferenca === null || diferenca === undefined) return 'grey'
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

// Função para carregar dados
const carregarDados = async () => {
  loading.value = true
  try {
    // Buscar produtos
    const produtosResponse = await api.get('/produtos/')
    console.log('Resposta da API de produtos:', produtosResponse.data)
    
    // Armazenar produtos
    if (produtosResponse.data.results && Array.isArray(produtosResponse.data.results)) {
      produtos.value = produtosResponse.data.results
      console.log('Produtos carregados:', produtos.value.length)
      
      // Expandir todos os painéis por padrão
      expandedPanels.value = Array.from({ length: produtosAgrupados.value.length }, (_, i) => i)
    } else {
      produtos.value = []
      console.warn('Nenhum produto retornado da API')
    }
  } catch (error) {
    console.error('Erro ao carregar dados:', error)
    console.error('Detalhes do erro:', error.response?.data)
  } finally {
    loading.value = false
  }
}

// Função para verificar preço de um produto
const verificarPreco = async (produtoId) => {
  verificandoItem.value = produtoId
  try {
    await api.post(`/produtos/${produtoId}/verificar/`)
    // Recarregar os dados após verificar o preço
    await carregarDados()
  } catch (error) {
    console.error('Erro ao verificar preço:', error)
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
</script>

<style scoped>
.produto-panel {
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

.produto-panel:hover {
  border-color: #bbdefb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.debug-btn {
  position: fixed;
  bottom: 16px;
  right: 16px;
  z-index: 100;
}

/* Personalização dos expansion panels */
:deep(.v-expansion-panel::before) {
  box-shadow: none !important;
}

:deep(.v-expansion-panel-header) {
  padding: 12px 16px;
}

:deep(.v-expansion-panel-content__wrap) {
  padding: 0;
}

/* Estilo para a tabela */
:deep(.v-data-table) {
  border-radius: 0;
}

:deep(.v-data-table th) {
  font-weight: bold !important;
  color: rgba(0, 0, 0, 0.7) !important;
  background-color: #f5f5f5;
}

:deep(.v-data-table tr:nth-child(even)) {
  background-color: #fafafa;
}

:deep(.v-data-table tr.cliente-row) {
  background-color: rgba(33, 150, 243, 0.05);
}
</style>