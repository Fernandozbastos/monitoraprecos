<template>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h4 mb-4">Dashboard</h1>
        </v-col>
      </v-row>
      
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
              Última Verificação
              <v-spacer></v-spacer>
              <v-icon color="primary">mdi-clock-outline</v-icon>
            </v-card-title>
            <v-card-text>
              <p class="text-h6 text-center">{{ ultimaVerificacao }}</p>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="12" md="4">
          <v-card class="mb-4" elevation="2">
            <v-card-title class="text-h6">
              Notificações
              <v-spacer></v-spacer>
              <v-icon color="primary">mdi-bell-outline</v-icon>
            </v-card-title>
            <v-card-text>
              <p class="text-h4 text-center">{{ notificacoes }}</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      
      <v-row>
        <v-col cols="12">
          <v-card elevation="2">
            <v-card-title class="text-h6">
              Últimos Preços Verificados
              <v-spacer></v-spacer>
              <v-btn icon :loading="loading" @click="carregarDados">
                <v-icon>mdi-refresh</v-icon>
              </v-btn>
            </v-card-title>
            <v-card-text>
              <v-data-table
                :headers="headers"
                :items="ultimosPrecos"
                :loading="loading"
                :items-per-page="5"
                class="elevation-0"
              >
                <template v-slot:item.preco="{ item }">
                  R$ {{ item.preco.toFixed(2) }}
                </template>
                <template v-slot:item.data="{ item }">
                  {{ formatDate(item.data) }}
                </template>
                <template v-slot:item.actions="{ item }">
                  <v-btn
                    small
                    text
                    color="primary"
                    @click="verDetalhes(item.produto)"
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
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import api from '@/services/api'
  
  const router = useRouter()
  const loading = ref(false)
  const totalProdutos = ref(0)
  const ultimaVerificacao = ref('-')
  const notificacoes = ref(0)
  const ultimosPrecos = ref([])
  
  const headers = [
    { title: 'Produto', key: 'produto_nome' },
    { title: 'Preço', key: 'preco' },
    { title: 'Data', key: 'data' },
    { title: 'Ações', key: 'actions', sortable: false }
  ]
  
  onMounted(() => {
    carregarDados()
  })
  
  const carregarDados = async () => {
    loading.value = true
    try {
      // Carregar total de produtos
      const produtosResponse = await api.get('/produtos/')
      totalProdutos.value = produtosResponse.data.count
      
      // Verificar última verificação
      if (produtosResponse.data.results && produtosResponse.data.results.length > 0) {
        const produtos = produtosResponse.data.results
        let ultimaData = null
        
        produtos.forEach(produto => {
          if (produto.ultima_verificacao) {
            const dataVerificacao = new Date(produto.ultima_verificacao)
            if (!ultimaData || dataVerificacao > ultimaData) {
              ultimaData = dataVerificacao
            }
          }
        })
        
        if (ultimaData) {
          ultimaVerificacao.value = formatDate(ultimaData)
        }
      }
      
      // Carregar últimos preços
      const historicosResponse = await api.get('/historico/?limit=10')
      ultimosPrecos.value = historicosResponse.data.results
      
      // Notificações (placeholder)
      notificacoes.value = 0
    } catch (error) {
      console.error('Erro ao carregar dados do dashboard:', error)
    } finally {
      loading.value = false
    }
  }
  
  const formatDate = (dateString) => {
    const options = { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }
    return new Date(dateString).toLocaleString('pt-BR', options)
  }
  
  const verDetalhes = (produtoId) => {
    router.push(`/products/${produtoId}`)
  }
  </script>