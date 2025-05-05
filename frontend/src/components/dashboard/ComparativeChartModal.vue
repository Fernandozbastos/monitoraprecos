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
          <!-- Filtro de período -->
          <v-row>
            <v-col cols="12" sm="4">
              <v-select
                v-model="periodoSelecionado"
                :items="periodos"
                item-title="label"
                item-value="value"
                label="Período"
                outlined
                dense
                hide-details
                class="mb-4"
                @update:modelValue="carregarDados"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="8">
              <div class="text-subtitle-2 text-grey d-flex align-center">
                <v-icon small color="primary" class="mr-2">mdi-chart-line</v-icon>
                Este gráfico mostra a evolução dos preços de todos os produtos deste grupo
              </div>
            </v-col>
          </v-row>
          
          <!-- Conteúdo do gráfico -->
          <div v-if="carregando" class="d-flex justify-center align-center py-12">
            <v-progress-circular indeterminate size="64" color="primary"></v-progress-circular>
            <span class="ml-4 text-subtitle-1">Carregando dados históricos...</span>
          </div>
          
          <div v-else-if="!dadosHistorico || !dadosHistorico.length" class="text-center py-12">
            <v-icon size="64" color="grey lighten-1">mdi-chart-timeline-variant</v-icon>
            <h3 class="text-h6 grey--text text--darken-1 mt-4">Nenhum dado histórico encontrado</h3>
            <p class="text-body-2 grey--text mb-4">Não há dados históricos disponíveis para este período</p>
          </div>
          
          <div v-else ref="chartContainer" style="height: 500px; width: 100%;">
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
  import { ref, watch, computed, onMounted, onUnmounted, nextTick } from 'vue'
  import Chart from 'chart.js/auto'
  import api from '@/services/api'
  
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
  const chartContainer = ref(null)
  const chartInstance = ref(null)
  
  // Períodos disponíveis
  const periodos = ref([
    { label: 'Últimos 7 dias', value: 7 },
    { label: 'Últimos 30 dias', value: 30 },
    { label: 'Últimos 60 dias', value: 60 },
    { label: 'Últimos 90 dias', value: 90 },
    { label: 'Todos', value: 'all' }
  ])
  const periodoSelecionado = ref(30)
  
  // Cores predefinidas para os diferentes produtos
  const cores = [
    '#1976D2', // Azul
    '#F57C00', // Laranja
    '#388E3C', // Verde
    '#7B1FA2', // Roxo
    '#D32F2F', // Vermelho
    '#0097A7', // Cyan
    '#FBC02D', // Amarelo
    '#455A64', // Cinza escuro
    '#E91E63', // Rosa
    '#795548'  // Marrom
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
  
  // Consolidar preços por dia (menor valor)
  const consolidarPorDia = (dados) => {
    if (!Array.isArray(dados) || dados.length === 0) return []
    
    const agrupados = {}
    
    dados.forEach(item => {
      const data = new Date(item.data)
      const dataKey = `${data.getFullYear()}-${data.getMonth()}-${data.getDate()}`
      
      const preco = parseFloat(item.preco)
      
      if (!agrupados[dataKey] || preco < agrupados[dataKey].preco) {
        agrupados[dataKey] = {
          data: item.data,
          preco: preco
        }
      }
    })
    
    return Object.values(agrupados).sort(
      (a, b) => new Date(a.data) - new Date(b.data)
    )
  }
  
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
            
            // Filtrar por período se não for 'all'
            if (periodoSelecionado.value !== 'all') {
              const dataLimite = new Date()
              dataLimite.setDate(dataLimite.getDate() - periodoSelecionado.value)
              
              dados = dados.filter(item => {
                const dataItem = new Date(item.data)
                return dataItem >= dataLimite
              })
            }
            
            if (dados.length > 0) {
              // Consolidar por dia
              const dadosConsolidados = consolidarPorDia(dados)
              
              historicos.push({
                produtoId: produto.id,
                nome: produto.nome,
                concorrente: produto.concorrente,
                tipoProduto: produto.tipo_produto,
                produtoCliente: produto.produto_cliente,
                dados: dadosConsolidados
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
      
      const data = historico.dados.map(item => ({
        x: new Date(item.data),
        y: item.preco
      }))
      
      // Determinar o estilo da linha com base no tipo de produto
      const estilo = historico.tipoProduto === 'cliente' || historico.produtoCliente
        ? {
            borderWidth: 4,
            pointRadius: 8,
            borderDash: [],  // Linha sólida
            pointBorderWidth: 3
          }
        : {
            borderWidth: 2,
            pointRadius: 5,
            borderDash: [5, 5], // Linha tracejada
            pointBorderWidth: 1
          }
      
      // Determinar o label
      const label = historico.tipoProduto === 'cliente' 
        ? `${historico.concorrente} (Cliente)` 
        : `${historico.concorrente}`
      
      return {
        label: label,
        data: data,
        borderColor: cor,
        backgroundColor: cor.replace('rgb', 'rgba').replace(')', ', 0.1)'),
        ...estilo,
        pointBackgroundColor: cor,
        pointBorderColor: '#ffffff',
        pointHoverRadius: 10,
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
              text: 'Data',
              font: {
                size: 14,
                weight: 'bold'
              }
            }
          },
          y: {
            beginAtZero: false,
            title: {
              display: true,
              text: 'Preço (R$)',
              font: {
                size: 14,
                weight: 'bold'
              }
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
              padding: 15,
              filter: function(item) {
                // Não filtrar nada, mostrar todos
                return true
              }
            }
          },
          title: {
            display: true,
            text: `Comparativo de Preços - ${props.grupo?.nome}`,
            font: {
              size: 16,
              weight: 'bold'
            },
            padding: {
              top: 10,
              bottom: 20
            }
          }
        },
        animation: {
          duration: 800,
          easing: 'easeInOutQuart'
        }
      }
    })
  }
  
  // Fechar modal
  const fecharModal = () => {
    internalShow.value = false
  }
  
  // Cleanup
  onUnmounted(() => {
    if (chartInstance.value) {
      chartInstance.value.destroy()
      chartInstance.value = null
    }
  })
  
  // Expor refs para uso externo
  defineExpose({
    chart,
    chartContainer
  })
  </script>
  
  <style scoped>
  /* Garantir que o container tenha tamanho */
  :deep(.v-card-text) {
    min-height: 600px;
  }
  
  canvas {
    display: block;
  }
  </style>