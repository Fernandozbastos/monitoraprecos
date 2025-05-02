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
      <v-card-text class="pa-4">
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
        
        <!-- Lista de produtos com resumo colapsável usando v-expansion-panels -->
        <v-expansion-panels v-if="produtosAgrupados.length > 0" multiple>
          <v-expansion-panel
            v-for="(grupo, index) in produtosAgrupados"
            :key="index"
            class="mb-3"
          >
            <v-expansion-panel-header>
              <div class="d-flex align-center w-100">
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
                  Por favor, defina o produto cliente
                </v-chip>
                
                <v-spacer></v-spacer>
                
                <!-- Resumo do produto (apenas se houver produto cliente base) -->
                <template v-if="grupo.produtoClienteBase">
                  <div class="d-none d-md-flex align-center">
                    <!-- Preço do cliente -->
                    <div class="text-center mx-3">
                      <div class="caption grey--text">Preço Cliente</div>
                      <div class="subtitle-1 font-weight-medium primary--text">
                        {{ formatarPreco(grupo.produtoClienteBase.preco_cliente) }}
                      </div>
                    </div>
                    
                    <!-- Menor preço concorrente -->
                    <div class="text-center mx-3">
                      <div class="caption grey--text">Menor Preço</div>
                      <div class="subtitle-1 font-weight-medium">
                        {{ formatarPreco(grupo.menorPrecoConcorrente) }}
                      </div>
                    </div>
                    
                    <!-- Diferença percentual -->
                    <div class="text-center mx-3" v-if="grupo.diferencaPercentual !== null">
                      <div class="caption grey--text">Variação</div>
                      <v-chip
                        x-small
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
                    
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          icon
                          x-small
                          color="warning"
                          class="ml-1"
                          v-bind="attrs"
                          v-on="on"
                          @click="definirProdutoClienteBase(item)"
                          :disabled="item.produto_cliente"
                        >
                          <v-icon>mdi-star</v-icon>
                        </v-btn>
                      </template>
                      <span>Definir como produto cliente base</span>
                    </v-tooltip>
                  </div>
                </template>
              </v-data-table>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-card-text>
    </v-card>
    
    <!-- Snackbar para mensagens -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
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
import { useStore } from 'vuex' // Adicione esta importação
import api from '@/services/api'

const router = useRouter()
const store = useStore()
const loading = ref(false)
const produtos = ref([])
const debug = ref(false)
const verificandoItem = ref(null)

// Estado para snackbar
const snackbar = ref({
  show: false,
  text: '',
  color: 'success',
  timeout: 3000
})

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
  
  // Primeiro, colete todos os nomes únicos de produtos
  produtos.value.forEach(p => nomesProdutos.add(p.nome))
  
  // Para cada nome de produto, crie um grupo
  Array.from(nomesProdutos).forEach(nome => {
    const produtosDesseTipo = produtos.value.filter(p => p.nome === nome)
    
    // Encontrar produto cliente base (marcado como produto_cliente)
    const produtoClienteBase = produtosDesseTipo.find(p => p.produto_cliente === true)
    
    // Produtos concorrentes
    const produtosConcorrentes = produtosDesseTipo.filter(p => p.tipo_produto === 'concorrente')
    
    // Encontrar o menor preço entre os concorrentes e o concorrente correspondente
    let menorPrecoConcorrente = null
    let concorrenteMenorPreco = null
    
    if (produtosConcorrentes.length > 0) {
      // Encontrar o menor preço e o concorrente correspondente
      let menorPreco = Number.MAX_SAFE_INTEGER
      let produtoConcorrenteMenorPreco = null
      
      produtosConcorrentes.forEach(p => {
        const preco = p.preco_ultimo || p.menor_preco_concorrente
        if (preco !== null && preco !== undefined && preco < menorPreco) {
          menorPreco = preco
          produtoConcorrenteMenorPreco = p
        }
      })
      
      if (menorPreco < Number.MAX_SAFE_INTEGER) {
        menorPrecoConcorrente = menorPreco
        concorrenteMenorPreco = produtoConcorrenteMenorPreco?.concorrente || null
      }
    }
    
    // Calcular a diferença percentual entre o preço do cliente base e o menor preço concorrente
    let diferencaPercentual = null
    if (produtoClienteBase && produtoClienteBase.preco_cliente && menorPrecoConcorrente) {
      diferencaPercentual = ((produtoClienteBase.preco_cliente - menorPrecoConcorrente) / menorPrecoConcorrente) * 100
    }
    
    // Processar cada produto para exibição na tabela
    const produtosProcessados = produtosDesseTipo.map(p => {
      let diferencaIndividual = null
      
      // Para produtos do cliente, calcular a diferença em relação ao menor preço concorrente
      if (p.tipo_produto === 'cliente' && p.preco_cliente && menorPrecoConcorrente) {
        diferencaIndividual = ((p.preco_cliente - menorPrecoConcorrente) / menorPrecoConcorrente) * 100
      }
      
      // Para produtos concorrentes, calcular a diferença em relação ao produto cliente base
      if (p.tipo_produto === 'concorrente' && produtoClienteBase && produtoClienteBase.preco_cliente) {
        const precoConcorrente = p.preco_ultimo || p.menor_preco_concorrente
        if (precoConcorrente) {
          diferencaIndividual = ((precoConcorrente - produtoClienteBase.preco_cliente) / produtoClienteBase.preco_cliente) * 100
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
      produtoClienteBase,
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

// Exibir mensagem no snackbar
const mostrarSnackbar = (texto, cor = 'success', timeout = 3000) => {
  snackbar.value = {
    show: true,
    text: texto,
    color: cor,
    timeout: timeout
  }
}

// Função para definir um produto como produto cliente base
const definirProdutoClienteBase = async (produto) => {
  try {
    console.log(`Iniciando atualização do produto ${produto.id} para cliente base`);
    
    // Verificar se existe um cliente atual selecionado
    if (!store.getters['auth/user']?.cliente_atual) {
      mostrarSnackbar('Por favor, selecione um cliente atual no menu superior antes de continuar', 'warning');
      return;
    }
    
    // Atualizar o produto com o novo status
    const response = await api.patch(`/produtos/${produto.id}/`, {
      produto_cliente: true
    });
    
    console.log('Atualização concluída com sucesso', response.data);
    
    // Recarregar dados após a atualização
    await carregarDados();
    
    mostrarSnackbar('Produto definido como base para comparações');
    
  } catch (error) {
    console.error('Erro ao definir produto cliente base:', error);
    
    // Tratamento específico de erros
    if (error.response) {
      console.error('Detalhes do erro:', error.response.data);
      
      // Mensagens de erro específicas baseadas na resposta do servidor
      if (error.response.status === 400) {
        const mensagem = error.response.data.detail || 'Verifique se você selecionou um cliente atual.';
        mostrarSnackbar(`Erro: ${mensagem}`, 'error');
      } 
      else if (error.response.status === 403) {
        mostrarSnackbar('Este produto não pertence ao cliente atual selecionado.', 'error');
      }
      else {
        mostrarSnackbar(`Erro ao definir produto cliente base: ${error.response.data.detail || 'Erro interno do servidor'}`, 'error');
      }
    } else {
      // Erro de conexão ou outro tipo
      mostrarSnackbar('Erro de conexão ao tentar atualizar o produto', 'error');
    }
  }
}

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
  // Usar a propriedade preco_exibicao que foi calculada no computed
  return formatarPreco(produto.preco_exibicao)
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
      
      // Para cada produto, recuperar o histórico de preços
      await Promise.all(produtos.value.map(async (produto) => {
        try {
          // Recuperar histórico de preços para este produto
          const historicoResponse = await api.get(`/produtos/${produto.id}/historico/`)
          produto.historico_precos = historicoResponse.data
          
          // Definir o preço mais recente como preco_ultimo
          if (historicoResponse.data.length > 0) {
            produto.preco_ultimo = historicoResponse.data[0].preco
          }
        } catch (error) {
          console.error(`Erro ao carregar histórico do produto ${produto.id}:`, error)
        }
      }))
    } else {
      produtos.value = []
      console.warn('Nenhum produto retornado da API')
    }
  } catch (error) {
    console.error('Erro ao carregar dados:', error)
    console.error('Detalhes do erro:', error.response?.data)
    mostrarSnackbar('Erro ao carregar dados', 'error')
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
</script>

<style scoped>
.debug-btn {
  position: fixed;
  bottom: 16px;
  right: 16px;
  z-index: 100;
}

/* Estilos para os expansion panels */
:deep(.v-expansion-panel::before) {
  box-shadow: none !important;
}

:deep(.v-expansion-panel-header) {
  padding: 12px 16px;
}

:deep(.v-expansion-panel-content__wrap) {
  padding: 0 16px 16px;
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
</style>