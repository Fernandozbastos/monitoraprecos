import { ref, onUnmounted, nextTick } from 'vue'
import Chart from 'chart.js/auto'
import api from '@/services/api'

export const usePriceHistory = () => {
  // Estado
  const historicoPrecos = ref([])
  const carregandoHistorico = ref(false)
  const priceChart = ref(null)
  const chartInstance = ref(null)
  const chartContainer = ref(null)
  
  // Carregar histórico completo de preços
  const carregarHistoricoCompleto = async (produtoId) => {
    if (!produtoId) return
    
    carregandoHistorico.value = true
    try {
      const historicoResponse = await api.get(`/produtos/${produtoId}/historico/?limit=100`)
      
      if (Array.isArray(historicoResponse.data)) {
        historicoPrecos.value = [...historicoResponse.data].sort(
          (a, b) => new Date(a.data) - new Date(b.data)
        )
        
        nextTick(() => {
          renderizarGrafico()
        })
      } else {
        console.error('Formato de resposta inesperado:', historicoResponse.data)
        historicoPrecos.value = []
      }
    } catch (error) {
      console.error('Erro ao carregar histórico completo:', error)
      historicoPrecos.value = []
      throw error
    } finally {
      carregandoHistorico.value = false
    }
  }
  
  // Renderizar o gráfico de histórico de preços
  const renderizarGrafico = () => {
    if (chartInstance.value) {
      chartInstance.value.destroy()
    }
    
    if (!priceChart.value || historicoPrecos.value.length === 0) return
    
    const ctx = priceChart.value.getContext('2d')
    
    // Preparar dados para o gráfico
    const labels = historicoPrecos.value.map(item => formatDateShort(item.data))
    const precos = historicoPrecos.value.map(item => parseFloat(item.preco))
    
    // Calcular preço mínimo e máximo para melhor exibição
    const maxPreco = Math.max(...precos) * 1.1 // 10% acima do máximo
    const minPreco = Math.min(...precos) * 0.9 // 10% abaixo do mínimo
    
    // Criar o gráfico
    chartInstance.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Preço (R$)',
          data: precos,
          backgroundColor: 'rgba(63, 81, 181, 0.2)',
          borderColor: 'rgba(63, 81, 181, 1)',
          borderWidth: 2,
          pointRadius: 4,
          pointBackgroundColor: 'rgba(63, 81, 181, 1)',
          tension: 0.3,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
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
            },
            suggestedMin: minPreco,
            suggestedMax: maxPreco
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
                return 'Preço: R$ ' + context.parsed.y.toFixed(2)
              }
            }
          },
          legend: {
            display: true,
            position: 'top'
          },
          title: {
            display: true,
            // Título será definido dinamicamente no componente
            text: '',
            font: {
              size: 16
            }
          }
        },
        animation: {
          duration: 1000
        }
      }
    })
  }
  
  // Formatação de data mais simples para o gráfico
  const formatDateShort = (dateString) => {
    if (!dateString) return ''
    const options = { day: '2-digit', month: '2-digit', year: '2-digit' }
    try {
      return new Date(dateString).toLocaleString('pt-BR', options)
    } catch (e) {
      console.error('Erro ao formatar data curta:', e)
      return dateString
    }
  }
  
  // Atualizar título do gráfico
  const atualizarTituloGrafico = (nome, concorrente) => {
    if (chartInstance.value) {
      chartInstance.value.options.plugins.title.text = `Histórico de Preços - ${nome} (${concorrente})`
      chartInstance.value.update()
    }
  }
  
  // Cleanup quando o componente for destruído
  onUnmounted(() => {
    if (chartInstance.value) {
      chartInstance.value.destroy()
      chartInstance.value = null
    }
  })
  
  // Resize handler
  const resizeChart = () => {
    if (chartInstance.value) {
      chartInstance.value.resize()
    }
  }
  
  return {
    // Estado
    historicoPrecos,
    carregandoHistorico,
    priceChart,
    chartContainer,
    
    // Métodos
    carregarHistoricoCompleto,
    renderizarGrafico,
    atualizarTituloGrafico,
    resizeChart
  }
}