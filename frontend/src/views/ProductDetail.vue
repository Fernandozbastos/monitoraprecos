<template>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-btn text @click="$router.go(-1)" class="mb-4">
            <v-icon left>mdi-arrow-left</v-icon>
            Voltar
          </v-btn>
          <h1 class="text-h4 mb-4">{{ produto.nome || 'Detalhes do Produto' }}</h1>
        </v-col>
      </v-row>
      
      <v-row v-if="loading">
        <v-col cols="12" class="text-center">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-col>
      </v-row>
      
      <template v-else>
        <v-row>
          <v-col cols="12" md="6">
            <v-card elevation="2" class="mb-4">
              <v-card-title>Informações do Produto</v-card-title>
              <v-card-text>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle>Nome</v-list-item-subtitle>
                    <v-list-item-title class="text-h6">{{ produto.nome }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle>Concorrente</v-list-item-subtitle>
                    <v-list-item-title>{{ produto.concorrente }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle>URL</v-list-item-subtitle>
                    <v-list-item-title>
                      <a :href="produto.url" target="_blank" rel="noopener noreferrer">
                        {{ produto.url }}
                      </a>
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle>Plataforma</v-list-item-subtitle>
                    <v-list-item-title>{{ produto.plataforma?.nome || 'N/A' }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle>Última Verificação</v-list-item-subtitle>
                    <v-list-item-title>{{ produto.ultima_verificacao ? formatDate(produto.ultima_verificacao) : 'Nunca' }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-card-text>
              <v-card-actions>
                <v-btn 
                  color="primary" 
                  @click="verificarPreco" 
                  :loading="verificando"
                >
                  <v-icon left>mdi-refresh</v-icon>
                  Verificar Preço Agora
                </v-btn>
                <v-btn 
                  text
                  color="secondary"
                  :href="produto.url" 
                  target="_blank"
                >
                  <v-icon left>mdi-open-in-new</v-icon>
                  Abrir Site
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card elevation="2" class="mb-4">
              <v-card-title>
                Última Verificação
                <v-spacer></v-spacer>
                <v-chip color="primary" v-if="historico.length > 0">
                  R$ {{ historico[0].preco.toFixed(2) }}
                </v-chip>
              </v-card-title>
              <v-card-text v-if="historico.length > 0">
                <p>Data: {{ formatDate(historico[0].data) }}</p>
                <p v-if="historico.length > 1">
                  Variação: 
                  <span :class="variacao >= 0 ? 'green--text' : 'red--text'">
                    {{ variacao >= 0 ? '+' : '' }}{{ variacao.toFixed(2) }}%
                  </span>
                </p>
              </v-card-text>
              <v-card-text v-else>
                <p>Nenhum histórico de preço disponível.</p>
              </v-card-text>
            </v-card>
            
            <v-card elevation="2">
              <v-card-title>Histórico de Preços</v-card-title>
              <v-card-text>
                <div v-if="historico.length > 0">
                  <canvas id="priceChart" ref="chartRef"></canvas>
                </div>
                <div v-else class="text-center">
                  <p>Nenhum histórico para exibir</p>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        
        <v-row>
          <v-col cols="12">
            <v-card elevation="2">
              <v-card-title>
                Tabela de Histórico
                <v-spacer></v-spacer>
                <v-btn icon :loading="carregandoHistorico" @click="carregarHistorico">
                  <v-icon>mdi-refresh</v-icon>
                </v-btn>
              </v-card-title>
              <v-card-text>
                <v-data-table
                  :headers="historicoHeaders"
                  :items="historico"
                  :loading="carregandoHistorico"
                  :items-per-page="10"
                  sort-by="data"
                  sort-desc
                  class="elevation-0"
                >
                  <template v-slot:item.preco="{ item }">
                    R$ {{ item.preco.toFixed(2) }}
                  </template>
                  <template v-slot:item.data="{ item }">
                    {{ formatDate(item.data) }}
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-container>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, watch } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { Chart, registerables } from 'chart.js'
  import api from '@/services/api'
  
  // Registra os componentes do Chart.js
  Chart.register(...registerables)
  
  const route = useRoute()
  const router = useRouter()
  const chartRef = ref(null)
  const chartInstance = ref(null)
  
  const loading = ref(false)
  const carregandoHistorico = ref(false)
  const verificando = ref(false)
  const produto = ref({})
  const historico = ref([])
  
  const historicoHeaders = [
    { title: 'Data', key: 'data' },
    { title: 'Preço', key: 'preco' }
  ]
  
  const variacao = computed(() => {
    if (historico.value.length < 2) return 0
    
    const precoAtual = historico.value[0].preco
    const precoAnterior = historico.value[1].preco
    
    return ((precoAtual - precoAnterior) / precoAnterior) * 100
  })
  
  onMounted(async () => {
    await carregarProduto()
    await carregarHistorico()
  })
  
  watch(historico, () => {
    renderChart()
  }, { deep: true })
  
  const carregarProduto = async () => {
    loading.value = true
    try {
      const response = await api.get(`/produtos/${route.params.id}/`)
      produto.value = response.data
    } catch (error) {
      console.error('Erro ao carregar produto:', error)
    } finally {
      loading.value = false
    }
  }
  
  const carregarHistorico = async () => {
    carregandoHistorico.value = true
    try {
      const response = await api.get(`/produtos/${route.params.id}/historico/`)
      historico.value = response.data
    } catch (error) {
      console.error('Erro ao carregar histórico:', error)
    } finally {
      carregandoHistorico.value = false
    }
  }
  
  const verificarPreco = async () => {
    verificando.value = true
    try {
      await api.post(`/produtos/${route.params.id}/verificar/`)
      // Atualiza os dados após verificação
      await carregarProduto()
      await carregarHistorico()
    } catch (error) {
      console.error('Erro ao verificar preço:', error)
    } finally {
      verificando.value = false
    }
  }
  
  const formatDate = (dateString) => {
    const options = { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }
    return new Date(dateString).toLocaleString('pt-BR', options)
  }
  
  const renderChart = () => {
    if (chartInstance.value) {
      chartInstance.value.destroy()
    }
  
    if (!chartRef.value || historico.value.length === 0) return
  
    const ctx = chartRef.value.getContext('2d')
    
    const dados = [...historico.value].reverse()
    
    chartInstance.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels: dados.map(item => new Date(item.data).toLocaleDateString('pt-BR')),
        datasets: [
          {
            label: 'Preço (R$)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: '#36A2EB',
            data: dados.map(item => item.preco),
            fill: true,
            tension: 0.1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: {
            beginAtZero: false,
            title: {
              display: true,
              text: 'Preço (R$)'
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
                return 'R$ ' + context.parsed.y.toFixed(2)
              }
            }
          }
        }
      }
    })
  }
  </script>