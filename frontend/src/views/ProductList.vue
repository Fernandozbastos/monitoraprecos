<template>
  <v-container fluid>
    <!-- Cabeçalho com visual melhorado -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="3" class="mb-6 gradient-header">
          <v-card-text class="pa-6">
            <div class="d-flex flex-wrap align-center">
              <div>
                <h1 class="text-h4 white--text mb-1">Produtos</h1>
                <p class="text-subtitle-1 white--text mb-0">Gerencie seus produtos e concorrentes</p>
              </div>
              <v-spacer></v-spacer>
              <div>
                <v-btn
                  color="white"
                  class="primary--text text-none px-4 mr-2"
                  :loading="loading"
                  @click="carregarProdutos"
                >
                  <v-icon left>mdi-refresh</v-icon>
                  Atualizar
                </v-btn>
                <v-btn
                  color="success"
                  dark
                  elevation="1"
                  class="text-none px-4"
                  @click="$router.push('/products/add')"
                >
                  <v-icon left>mdi-plus</v-icon>
                  Adicionar Produto
                </v-btn>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Tabela de produtos com visual aprimorado -->
    <v-card elevation="2" class="mb-4">
      <v-card-title>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Pesquisar produtos..."
          single-line
          hide-details
          outlined
          dense
          clearable
          class="search-field"
        ></v-text-field>
        <v-spacer></v-spacer>
        <v-chip-group
          v-model="selectedTypes"
          multiple
          column
        >
          <v-chip
            filter
            outlined
            color="primary"
          >
            Cliente
          </v-chip>
          <v-chip
            filter
            outlined
            color="secondary"
          >
            Concorrente
          </v-chip>
        </v-chip-group>
      </v-card-title>
      
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="produtosFiltrados"
          :loading="loading"
          :search="search"
          :items-per-page="15"
          sort-by="nome"
          class="elevation-0 product-table"
          :loading-text="'Carregando produtos...'"
          :no-data-text="'Nenhum produto encontrado'"
          :footer-props="{
            'items-per-page-options': [10, 15, 20, 50],
            'items-per-page-text': 'Produtos por página'
          }"
        >
          <!-- Status do produto -->
          <template v-slot:item.tipo_produto="{ item }">
            <v-chip
              small
              :color="item.tipo_produto === 'cliente' ? 'primary' : 'grey lighten-1'"
              :text-color="item.tipo_produto === 'cliente' ? 'white' : 'grey darken-3'"
              class="px-2"
            >
              {{ item.tipo_produto === 'cliente' ? 'Cliente' : 'Concorrente' }}
            </v-chip>
          </template>
          
          <!-- Nome com tooltip para nomes longos -->
          <template v-slot:item.nome="{ item }">
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <span 
                  v-bind="attrs"
                  v-on="on"
                  class="product-name-cell"
                >
                  {{ item.nome }}
                  <v-icon 
                    v-if="item.produto_cliente" 
                    small 
                    color="amber darken-2" 
                    class="ml-1"
                  >
                    mdi-star
                  </v-icon>
                </span>
              </template>
              <span>{{ item.nome }}</span>
            </v-tooltip>
          </template>
          
          <!-- URL com link clicável -->
          <template v-slot:item.url="{ item }">
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <div 
                  v-bind="attrs"
                  v-on="on"
                  class="url-cell"
                >
                  <a 
                    :href="item.url" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    class="text-decoration-none text-truncate d-block"
                  >
                    {{ formatUrl(item.url) }}
                  </a>
                </div>
              </template>
              <span>{{ item.url }}</span>
            </v-tooltip>
          </template>
          
          <!-- Status do tipo de verificação -->
          <template v-slot:item.verificacao_manual="{ item }">
            <v-tooltip bottom :color="item.verificacao_manual ? 'warning' : 'success'">
              <template v-slot:activator="{ on, attrs }">
                <v-icon 
                  v-bind="attrs"
                  v-on="on"
                  :color="item.verificacao_manual ? 'warning' : 'success'"
                >
                  {{ item.verificacao_manual ? 'mdi-hand' : 'mdi-robot' }}
                </v-icon>
              </template>
              <span>{{ item.verificacao_manual ? 'Verificação Manual' : 'Verificação Automática' }}</span>
            </v-tooltip>
          </template>
          
          <!-- Última verificação com formatação -->
          <template v-slot:item.ultima_verificacao="{ item }">
            <div class="d-flex align-center">
              <v-icon 
                small 
                :color="getVerificationStatusColor(item.ultima_verificacao)" 
                class="mr-2"
              >
                {{ getVerificationStatusIcon(item.ultima_verificacao) }}
              </v-icon>
              <span>{{ formatDate(item.ultima_verificacao) }}</span>
            </div>
          </template>
          
          <!-- Coluna de ações -->
          <template v-slot:item.actions="{ item }">
            <div class="actions-cell">
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    icon
                    small
                    color="primary"
                    v-bind="attrs"
                    v-on="on"
                    @click="verDetalhes(item.id)"
                    class="mx-1"
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
                    small
                    color="success"
                    v-bind="attrs"
                    v-on="on"
                    @click="verificarPreco(item.id)"
                    :loading="verificandoItem === item.id"
                    class="mx-1"
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
                    small
                    color="warning"
                    v-bind="attrs"
                    v-on="on"
                    @click="$router.push(`/products/${item.id}/edit`)"
                    class="mx-1"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </template>
                <span>Editar produto</span>
              </v-tooltip>
            </div>
          </template>
          
          <!-- Status quando tabela estiver vazia -->
          <template v-slot:no-data>
            <div class="text-center py-6">
              <v-img
                src="@/assets/empty-products.svg"
                max-width="200"
                class="mx-auto mb-4"
              ></v-img>
              <h3 class="text-h5 grey--text text--darken-1 mb-2">Nenhum produto encontrado</h3>
              <p class="text-body-1 grey--text mb-4">Comece adicionando seu primeiro produto</p>
              <v-btn
                color="primary"
                @click="$router.push('/products/add')"
              >
                <v-icon left>mdi-plus</v-icon>
                Adicionar Produto
              </v-btn>
            </div>
          </template>
          
          <!-- Status quando a tabela estiver carregando -->
          <template v-slot:progress>
            <v-overlay :value="loading" absolute color="white" opacity="0.8">
              <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
            </v-overlay>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
    
    <!-- Snackbar para notificações -->
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()
const loading = ref(false)
const produtos = ref([])
const search = ref('')
const verificandoItem = ref(null)
const selectedTypes = ref([]) // Filtro por tipo de produto

// Estado do snackbar
const snackbar = ref({
  show: false,
  text: '',
  color: 'success',
  timeout: 4000
})

// Cabeçalhos da tabela
const headers = [
  { text: 'Tipo', value: 'tipo_produto', width: '100px', align: 'center' },
  { text: 'Nome', value: 'nome' },
  { text: 'Concorrente', value: 'concorrente' },
  { text: 'Plataforma', value: 'plataforma_nome', width: '150px' },
  { text: 'URL', value: 'url' },
  { text: 'Verificação', value: 'verificacao_manual', width: '100px', align: 'center' },
  { text: 'Última Verificação', value: 'ultima_verificacao', width: '200px' },
  { text: 'Ações', value: 'actions', sortable: false, align: 'center', width: '150px' }
]

// Produtos filtrados por tipo (cliente/concorrente)
const produtosFiltrados = computed(() => {
  if (selectedTypes.value.length === 0) {
    return produtos.value
  }
  
  // Mapear seleção para tipos reais
  const tiposFiltrados = []
  if (selectedTypes.value.includes(0)) tiposFiltrados.push('cliente')
  if (selectedTypes.value.includes(1)) tiposFiltrados.push('concorrente')
  
  return produtos.value.filter(produto => tiposFiltrados.includes(produto.tipo_produto))
})

// Inicialização
onMounted(() => {
  carregarProdutos()
})

// Carregar produtos
const carregarProdutos = async () => {
  loading.value = true
  try {
    // Prevenir cache adicionando timestamp
    const timestamp = new Date().getTime()
    const response = await api.get(`/produtos/?t=${timestamp}`)
    
    if (response.data.results && Array.isArray(response.data.results)) {
      produtos.value = response.data.results
    } else {
      produtos.value = []
    }
  } catch (error) {
    console.error('Erro ao carregar produtos:', error)
    mostrarSnackbar('Erro ao carregar produtos', 'error')
  } finally {
    loading.value = false
  }
}

// Formatar URL para exibição compacta
const formatUrl = (url) => {
  if (!url) return '';
  try {
    // Remover protocolo e www
    let formatted = url.replace(/^https?:\/\//i, '').replace(/^www\./i, '')
    // Limitar tamanho
    if (formatted.length > 30) {
      formatted = formatted.substring(0, 30) + '...'
    }
    return formatted
  } catch (e) {
    return url
  }
}

// Formatar data de verificação
const formatDate = (dateString) => {
  if (!dateString) return 'Nunca verificado'
  try {
    const options = { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }
    return new Date(dateString).toLocaleString('pt-BR', options)
  } catch (error) {
    return dateString || 'Data inválida'
  }
}

// Obter cor para status de verificação
const getVerificationStatusColor = (date) => {
  if (!date) return 'grey'
  
  const now = new Date()
  const verificationDate = new Date(date)
  const diffHours = (now - verificationDate) / (1000 * 60 * 60)
  
  if (diffHours < 24) return 'success'
  if (diffHours < 72) return 'warning'
  return 'error'
}

// Obter ícone para status de verificação
const getVerificationStatusIcon = (date) => {
  if (!date) return 'mdi-alert-circle-outline'
  
  const now = new Date()
  const verificationDate = new Date(date)
  const diffHours = (now - verificationDate) / (1000 * 60 * 60)
  
  if (diffHours < 24) return 'mdi-check-circle-outline'
  if (diffHours < 72) return 'mdi-clock-alert-outline'
  return 'mdi-alert-circle-outline'
}

// Exibir mensagem no snackbar
const mostrarSnackbar = (texto, cor = 'success', timeout = 4000) => {
  snackbar.value = {
    show: true,
    text: texto,
    color: cor,
    timeout: timeout
  }
}

// Navegar para detalhes do produto
const verDetalhes = (id) => {
  router.push(`/products/${id}`)
}

// Verificar preço do produto
const verificarPreco = async (id) => {
  verificandoItem.value = id
  try {
    await api.post(`/produtos/${id}/verificar/`)
    // Recarregar dados após verificação
    await carregarProdutos()
    mostrarSnackbar('Preço verificado com sucesso', 'success')
  } catch (error) {
    console.error('Erro ao verificar preço:', error)
    mostrarSnackbar('Erro ao verificar preço', 'error')
  } finally {
    verificandoItem.value = null
  }
}
</script>

<style scoped>
.gradient-header {
  background: linear-gradient(135deg, var(--v-primary-base) 0%, var(--v-primary-darken1) 100%);
  border-radius: 8px;
}

.search-field {
  max-width: 400px;
}

.product-table {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.v-data-table th) {
  font-weight: bold !important;
  color: rgba(0, 0, 0, 0.7) !important;
  background-color: #f5f5f5;
  text-transform: uppercase;
  font-size: 0.75rem;
}

:deep(.v-data-table tr:hover) {
  background-color: #f5f7fa !important;
}

:deep(.v-data-table tr:nth-child(even)) {
  background-color: #fafafa;
}

.product-name-cell {
  font-weight: 500;
  color: var(--v-primary-base);
  display: block;
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.url-cell {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.actions-cell {
  display: flex;
  justify-content: center;
}

.v-chip {
  font-size: 0.75rem !important;
}
</style>