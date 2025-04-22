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
      
      <!-- Tabela de produtos -->
      <v-row>
        <v-col cols="12">
          <v-card elevation="2">
            <v-card-title class="text-h6">
              Produtos Monitorados
              <v-spacer></v-spacer>
              <v-btn icon :loading="loading" @click="carregarDados">
                <v-icon>mdi-refresh</v-icon>
              </v-btn>
            </v-card-title>
            <v-card-text>
              <v-data-table
                :headers="headers"
                :items="produtos"
                :loading="loading"
                :items-per-page="10"
                class="elevation-0"
              >
                <template v-slot:item.concorrente="{ item }">
                  {{ item.concorrente }}
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
  import { ref, onMounted, onBeforeUnmount } from 'vue'
  import { useRouter } from 'vue-router'
  import axios from 'axios'
  
  const router = useRouter()
  const loading = ref(false)
  const totalProdutos = ref(0)
  const ultimaVerificacao = ref('-')
  const notificacoes = ref(0)
  const produtos = ref([])
  
  // Definição das colunas da tabela
  const headers = [
    { title: 'Nome', key: 'nome' },
    { title: 'Concorrente', key: 'concorrente' },
    { title: 'Última Verificação', key: 'ultima_verificacao' },
    { title: 'Ações', key: 'actions', sortable: false }
  ]
  
  // Montar o componente - versão segura
  onMounted(() => {
    try {
      carregarDados()
    } catch (error) {
      console.error('Erro ao montar componente:', error)
    }
  })
  
  // Prevenir erros ao desmontar o componente
  onBeforeUnmount(() => {
    // Limpeza de recursos, se necessário
  })
  
  // Formatar data com segurança
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
  
  // Função para carregar dados com tratamento de erros
  const carregarDados = async () => {
    loading.value = true
    try {
      // URL base da API
      const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
      
      // Token de autenticação do localStorage
      const token = localStorage.getItem('accessToken')
      if (!token) {
        console.error('Token não encontrado, redirecionando para login')
        router.push('/login')
        return
      }
      
      const config = {
        headers: { Authorization: `Bearer ${token}` }
      }
      
      // Carregar produtos
      try {
        console.log('Buscando produtos em:', `${baseURL}/produtos/`)
        const produtosResponse = await axios.get(`${baseURL}/produtos/`, config)
        console.log('Resposta da API:', produtosResponse.data)
        
        // Armazenar o total
        totalProdutos.value = produtosResponse.data.count || 0
        
        // Armazenar a lista de produtos
        if (produtosResponse.data.results && Array.isArray(produtosResponse.data.results)) {
          produtos.value = produtosResponse.data.results
          console.log('Produtos carregados:', produtos.value.length)
        } else {
          console.warn('Formato de resposta inesperado para produtos:', produtosResponse.data)
          produtos.value = []
        }
        
        // Verificar última verificação
        if (produtos.value.length > 0) {
          let ultimaData = null
          
          produtos.value.forEach(produto => {
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
      } catch (error) {
        console.error('Erro ao carregar produtos:', error.response || error.message || error)
        totalProdutos.value = '-'
        produtos.value = []
      }
      
      // Notificações (placeholder)
      notificacoes.value = 0
      
    } catch (error) {
      console.error('Erro geral ao carregar dados do dashboard:', error)
    } finally {
      loading.value = false
    }
  }
  
  const verDetalhes = (produtoId) => {
    if (produtoId) {
      console.log('Navegando para detalhes do produto:', produtoId)
      router.push(`/products/${produtoId}`)
    } else {
      console.error('ID do produto não disponível')
    }
  }
  
  // Expor funções publicamente para depuração
  window.dashboard = {
    carregarDados,
    produtos
  }
  </script>
  
  <style scoped>
  /* Estilos adicionais, se necessário */
  .text-h4 {
    font-weight: 500;
  }
  </style>