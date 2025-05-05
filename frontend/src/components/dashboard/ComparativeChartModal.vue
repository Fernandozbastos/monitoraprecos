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
          <!-- Conteúdo do gráfico -->
          <div v-if="carregando" class="d-flex justify-center align-center py-12">
            <v-progress-circular indeterminate size="64" color="primary"></v-progress-circular>
            <span class="ml-4 text-subtitle-1">Carregando dados históricos...</span>
          </div>
          
          <div v-else-if="!dadosHistorico.length" class="text-center py-12">
            <v-icon size="64" color="grey lighten-1">mdi-chart-timeline-variant</v-icon>
            <h3 class="text-h6 grey--text text--darken-1 mt-4">Nenhum dado histórico encontrado</h3>
            <p class="text-body-2 grey--text mb-4">Não há dados históricos disponíveis para este grupo</p>
          </div>
          
          <div v-else>
            <div ref="chartContainer" style="height: 500px; width: 100%;">
              <canvas ref="chart"></canvas>
            </div>
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
  
  // Cores predefinidas para os diferentes produtos
  const cores = [
    '#1976D2', '#F57C00', '#388E3C', '#7B1FA2', '#D32F2F', 
    '#0097A7', '#FBC02D', '#455A64', '#E91E63', '#795548'
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
            const dadosConsolidados = consolidarPorDia(response.data)
            
            historicos.push({
              produtoId: produto.id,
              nome: produto.nome,
              concorrente: produto.concorrente,
              tipoProduto: produto.tipo_produto,
              produtoCliente: produto.produto_cliente,
              dados: dadosConsolidados
            })
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
  
  // Formatar data para o gráfico
  const formatarData = (dataString) => {
    const data = new Date(dataString)
    const dia = data.getDate().toString().padStart(2, '0')
    const mes = (data.getMonth() + 1).toString().padStart(2, '0')
    return `${dia}/${mes}`
  }
  
  // Renderizar o gráfico comparativo
  const renderizarGrafico = () => {
    if (chartInstance.value) {
      chartInstance.value.destroy()
    }
    
    if (!chart.value || dadosHistorico.value.length === 0) return
    
    const ctx = chart.value.getContext('2d')
    
    // Coletar todas as datas únicas
    const todasDatas = new Set()
    dadosHistorico.value.forEach(historico => {
      historico.dados.forEach(item => {
        todasDatas.add(item.data)
      })
    })
    
    // Ordenar datas
    const datasOrdenadas = Array.from(todasDatas).sort((a, b) => new Date(a) - new Date(b))
    const labels = datasOrdenadas.map(data => formatarData(data))
    
    const datasets = dadosHistorico.value.map((historico, index) => {
      const cor = cores[index % cores.length]
      
      // Criar array de dados onde cada posição corresponde a uma data
      const data = datasOrdenadas.map(dataAtual => {
        const item = historico.dados.find(d => d.data === dataAtual)
        return item ? item.preco : null
      })
      
      // Determinar o estilo da linha com base no tipo de produto
      const estilo = historico.tipoProduto === 'cliente' 
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
        backgroundColor: cor + '20',
        ...estilo,
        pointBackgroundColor: cor,
        pointBorderColor: '#ffffff',
        pointHoverRadius: 10,
        tension: 0.3,
        fill: false,
        spanGaps: true // Permite que o gráfico conecte pontos mesmo com valores null
      }
    })
    
    chartInstance.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
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
              padding: 15
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
  canvas {
    display: block;
  }
  </style>