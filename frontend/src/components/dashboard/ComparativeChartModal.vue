<template>
    <v-dialog
      v-model="internalShow"
      max-width="1200px"
      scrollable
    >
      <v-card>
        <v-card-title class="primary white--text">
          <span>Histórico Comparativo de Preços - {{ grupo?.nome }}</span>
          <v-spacer></v-spacer>
          <v-btn
            icon
            color="white"
            @click="fecharModal"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        
        <v-card-text class="pa-6">
          <!-- Filtros superiores -->
          <v-row class="mb-4">
            <v-col cols="12" sm="6" md="4">
              <v-select
                v-model="filtros.periodo"
                :items="opcoesperiodo"
                item-text="text"
                item-value="value"
                outlined
                dense
                label="Período"
                prepend-icon="mdi-calendar"
              ></v-select>
            </v-col>
          </v-row>
  
          <!-- Conteúdo do gráfico -->
          <v-progress-linear
            v-if="carregando"
            indeterminate
            color="primary"
            class="mb-4"
          ></v-progress-linear>
          
          <div v-if="!carregando && !dadosHistorico.length" class="text-center py-12">
            <v-icon size="64" color="grey lighten-1">mdi-chart-timeline-variant</v-icon>
            <h3 class="text-h6 grey--text text--darken-1 mt-4">Nenhum dado histórico encontrado</h3>
            <p class="text-body-2 grey--text mb-4">Não há dados históricos disponíveis para este grupo</p>
          </div>
          
          <div v-if="dadosHistorico.length" class="chart-container">
            <canvas ref="chart"></canvas>
          </div>
        </v-card-text>
        
        <v-card-actions class="pa-4">
          <v-btn
            text
            color="grey darken-1"
            @click="fecharModal"
          >
            Fechar
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            @click="carregarDados"
            :loading="carregando"
          >
            <v-icon left>mdi-refresh</v-icon>
            Atualizar Gráfico
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script setup>
  import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
  import { Chart, registerables } from 'chart.js'
  import 'chartjs-adapter-date-fns'
  import api from '@/services/api'
  
  // Registrar os módulos do Chart.js
  Chart.register(...registerables)
  
  const props = defineProps({
    show: {
      type: Boolean,
      required: true
    },
    grupo: {
      type: Object,
      default: null
    }
  })
  
  const emit = defineEmits(['update:show'])
  
  // Estado interno
  const internalShow = ref(props.show)
  const carregando = ref(false)
  const dadosHistorico = ref([])
  const chart = ref(null)
  const chartInstance = ref(null)
  
  // Filtros
  const filtros = ref({
    periodo: '30'
  })
  
  const opcoesperiodo = ref([
    { text: 'Últimos 7 dias', value: '7' },
    { text: 'Últimos 30 dias', value: '30' },
    { text: 'Últimos 90 dias', value: '90' },
    { text: 'Todo período', value: 'all' }
  ])
  
  // Cores para os diferentes produtos
  const cores = [
    'rgba(63, 81, 181, 1)',    // Azul
    'rgba(255, 87, 34, 1)',    // Laranja
    'rgba(76, 175, 80, 1)',    // Verde
    'rgba(156, 39, 176, 1)',   // Roxo
    'rgba(233, 30, 99, 1)',    // Rosa
    'rgba(0, 150, 136, 1)',    // Teal
    'rgba(255, 193, 7, 1)',    // Amarelo
    'rgba(96, 125, 139, 1)',   // Cinza azulado
  ]
  
  // Sincronizar props com estado interno
  watch(() => props.show, (newVal) => {
    internalShow.value = newVal
    if (newVal && props.grupo) {
      carregarDados()
    }
  })
  
  watch(internalShow, (newVal) => {
    emit('update:show', newVal)
    if (!newVal && chartInstance.value) {
      chartInstance.value.destroy()
      chartInstance.value = null
    }
  })
  
  // Watch para mudanças no filtro de período
  watch(() => filtros.value.periodo, () => {
    carregarDados()
  })
  
  // Carregar dados históricos do grupo
  const carregarDados = async () => {
    if (!props.grupo?.produtos?.length) {
      dadosHistorico.value = []
      return
    }
    
    carregando.value = true
    
    try {
      const historicos = []
      
      // Carregar dados de todos os produtos do grupo
      for (const produto of props.grupo.produtos) {
        try {
          const response = await api.get(`/produtos/${produto.id}/historico/?limit=100`)
          
          if (Array.isArray(response.data) && response.data.length > 0) {
            let dados = [...response.data]
            
            // Filtrar por período
            if (filtros.value.periodo !== 'all') {
              const dias = parseInt(filtros.value.periodo)
              const dataLimite = new Date()
              dataLimite.setDate(dataLimite.getDate() - dias)
              
              dados = dados.filter(item => {
                const dataItem = new Date(item.data)
                return dataItem >= dataLimite
              })
            }
            
            if (dados.length > 0) {
              // Ordenar dados por data
              const dadosOrdenados = dados.sort((a, b) => new Date(a.data) - new Date(b.data))
              
              historicos.push({
                produtoId: produto.id,
                nome: produto.nome,
                concorrente: produto.concorrente,
                tipoProduto: produto.tipo_produto,
                produtoCliente: produto.produto_cliente,
                dados: dadosOrdenados
              })
            }
          }
        } catch (error) {
          console.error(`Erro ao carregar histórico do produto ${produto.id}:`, error)
        }
      }
      
      dadosHistorico.value = historicos
      
      if (historicos.length > 0) {
        nextTick(() => {
          renderizarGrafico()
        })
      }
      
    } catch (error) {
      console.error('Erro ao carregar dados históricos:', error)
    } finally {
      carregando.value = false
    }
  }
  
  // Renderizar o gráfico comparativo
  const renderizarGrafico = () => {
    if (chartInstance.value) {
      chartInstance.value.destroy()
    }
    
    if (!chart.value || dadosHistorico.value.length === 0) return
    
    const ctx = chart.value.getContext('2d')
    
    const datasets = dadosHistorico.value.map((historico, index) => {
      const cor = cores[index % cores.length]
      
      const dados = historico.dados.map(item => ({
        x: new Date(item.data),
        y: parseFloat(item.preco)
      }))
      
      // Determinar o tipo de linha com base no tipo de produto
      const lineType = historico.tipoProduto === 'cliente' ? {
        borderWidth: 3,
        pointRadius: 5,
        borderDash: []  // Linha sólida
      } : {
        borderWidth: 2,
        pointRadius: 3,
        borderDash: [5, 5]  // Linha tracejada
      }
      
      return {
        label: `${historico.concorrente} (${historico.tipoProduto === 'cliente' ? 'Cliente' : 'Concorrente'})`,
        data: dados,
        borderColor: cor,
        backgroundColor: cor.replace('1)', '0.1)'),
        ...lineType,
        pointBackgroundColor: cor,
        pointBorderColor: '#fff',
        pointHoverRadius: 8,
        tension: 0.3,
        fill: false
      }
    })
    
    chartInstance.value = new Chart(ctx, {
      type: 'line',
      data: {
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: 'index',
          intersect: false,
        },
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'day',
              displayFormats: {
                day: 'dd/MM'
              }
            },
            title: {
              display: true,
              text: 'Data'
            }
          },
          y: {
            beginAtZero: false,
            title: {
              display: true,
              text: 'Preço (R$)'
            },
            ticks: {
              callback: function(value) {
                return 'R$ ' + value.toFixed(2)
              }
            }
          }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function(context) {
                const value = context.parsed.y
                return `${context.dataset.label}: R$ ${value.toFixed(2)}`
              }
            }
          },
          legend: {
            display: true,
            position: 'top',
            labels: {
              usePointStyle: true,
              padding: 15
            }
          },
          title: {
            display: true,
            text: `Histórico de Preços - ${props.grupo?.nome}`,
            font: {
              size: 16
            },
            padding: {
              top: 10,
              bottom: 20
            }
          }
        },
        animation: {
          duration: 1000
        }
      }
    })
  }
  
  // Fechar modal
  const fecharModal = () => {
    internalShow.value = false
  }
  
  // Cleanup quando destruído
  onUnmounted(() => {
    if (chartInstance.value) {
      chartInstance.value.destroy()
      chartInstance.value = null
    }
  })
  
  // Expor refs para uso externo
  defineExpose({
    chart
  })
  </script>
  
  <style scoped>
  .chart-container {
    position: relative;
    height: 500px;
    width: 100%;
  }
  
  canvas {
    display: block;
  }
  </style>