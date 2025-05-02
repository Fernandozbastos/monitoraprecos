<template>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h4 mb-4">Dashboard</h1>
        </v-col>
      </v-row>
      
      <!-- Cards de informações -->
      <v-row>
        <v-col cols="12" md="4">
          <v-card class="mb-4" elevation="2">
            <v-card-title class="text-h6">
              Total de Produtos
              <v-spacer></v-spacer>
              <v-icon color="primary">mdi-package-variant-closed</v-icon>
            </v-card-title>
            <v-card-text>
              <p class="text-h4 text-center">{{ totalProdutos }}</p>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="12" md="4">
          <v-card class="mb-4" elevation="2">
            <v-card-title class="text-h6">
              Produtos com Vantagem
              <v-spacer></v-spacer>
              <v-icon color="success">mdi-thumb-up</v-icon>
            </v-card-title>
            <v-card-text>
              <p class="text-h4 text-center">{{ produtosComVantagem }}</p>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="12" md="4">
          <v-card class="mb-4" elevation="2">
            <v-card-title class="text-h6">
              Produtos em Desvantagem
              <v-spacer></v-spacer>
              <v-icon color="error">mdi-thumb-down</v-icon>
            </v-card-title>
            <v-card-text>
              <p class="text-h4 text-center">{{ produtosEmDesvantagem }}</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      
      <!-- Tabela de produtos com comparação de preços -->
      <v-row>
        <v-col cols="12">
          <v-card elevation="2">
            <v-card-title class="text-h6">
              Comparação de Preços
              <v-spacer></v-spacer>
              <v-btn icon :loading="loading" @click="carregarDados">
                <v-icon>mdi-refresh</v-icon>
              </v-btn>
            </v-card-title>
            <v-card-text>
              <v-data-table
                :headers="headers"
                :items="produtosCliente"
                :loading="loading"
                :items-per-page="10"
                class="elevation-0"
              >
                <template v-slot:item.preco_cliente="{ item }">
                  {{ formatarPreco(item.preco_cliente) }}
                </template>
                
                <template v-slot:item.menor_preco_concorrente="{ item }">
                  {{ formatarPreco(item.menor_preco_concorrente) }}
                </template>
                
                <template v-slot:item.diferenca_percentual="{ item }">
                  <v-chip
                    :color="getCorDiferenca(item.diferenca_percentual)"
                    small
                    v-if="item.diferenca_percentual !== null"
                  >
                    {{ formatarPercentual(item.diferenca_percentual) }}
                  </v-chip>
                  <span v-else>-</span>
                </template>
                
                <template v-slot:item.ultima_verificacao="{ item }">
                  {{ formatDate(item.ultima_verificacao) }}
                </template>
                
                <template v-slot:item.actions="{ item }">
                  <v-btn
                    small
                    text
                    color="primary"
                    @click="verDetalhes(item.id)"
                  >
                    Ver detalhes
                  </v-btn>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import api from '@/services/api'
  
  const router = useRouter()
  const loading = ref(false)
  const totalProdutos = ref(0)
  const produtos = ref([])
  
  // Produtos filtrados apenas pelos produtos do cliente
  const produtosCliente = computed(() => {
    return produtos.value.filter(produto => produto.tipo_produto === 'cliente')
  })
  
  // Contadores
  const produtosComVantagem = computed(() => {
    return produtosCliente.value.filter(p => 
      p.diferenca_percentual !== null && p.diferenca_percentual <= 0
    ).length
  })
  
  const produtosEmDesvantagem = computed(() => {
    return produtosCliente.value.filter(p => 
      p.diferenca_percentual !== null && p.diferenca_percentual > 0
    ).length
  })
  
  // Definição das colunas da tabela
  const headers = [
    { title: 'Nome', key: 'nome' },
    { title: 'Preço Cliente', key: 'preco_cliente' },
    { title: 'Menor Preço Concorrente', key: 'menor_preco_concorrente' },
    { title: 'Diferença', key: 'diferenca_percentual' },
    { title: 'Última Verificação', key: 'ultima_verificacao' },
    { title: 'Ações', key: 'actions', sortable: false }
  ]
  
  // Montar o componente
  onMounted(() => {
    carregarDados()
  })
  
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
    if (diferenca === null || diferenca === undefined) return ''
    return diferenca <= 0 ? 'success' : 'error'
  }
  
  // Formatar data
  const formatDate = (dateString) => {
    if (!dateString) return 'Nunca'
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
      
      // Atualizar dados
      totalProdutos.value = produtosResponse.data.count || 0
      
      // Armazenar produtos
      if (produtosResponse.data.results && Array.isArray(produtosResponse.data.results)) {
        produtos.value = produtosResponse.data.results
      } else {
        produtos.value = []
      }
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
    } finally {
      loading.value = false
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
  .v-chip {
    font-weight: bold;
  }
  </style>