import { ref, nextTick, onUnmounted } from 'vue'
import Chart from 'chart.js/auto'
import api from '@/services/api'

export const usePriceHistory = () => {
  // Estado
  const historicoPrecos = ref([])
  const carregandoHistorico = ref(false)
  const priceChart = ref(null)
  const chartInstance = ref(null)
  const chartContainer = ref(null)
  
  // Debug state
  const debugInfo = ref('')
  
  // Carregar histórico completo de preços
  const carregarHistoricoCompleto = async (produtoId) => {
    if (!produtoId) {
      debugInfo.value = 'Produto ID não fornecido'
      return
    }
    
    carregandoHistorico.value = true
    try {
      const historicoResponse = await api.get(`/produtos/${produtoId}/historico/?limit=100`)
      debugInfo.value = `API Response: ${JSON.stringify(historicoResponse.data?.length || '0')} registros`
      
      if (Array.isArray(historicoResponse.data)) {
        historicoPrecos.value = [...historicoResponse.data].sort(
          (a, b) => new Date(a.data) - new Date(b.data)
        )
        
        debugInfo.value += ` | Dados ordenados: ${historicoPrecos.value.length}`
        
        // Verificar se o canvas está disponível antes de renderizar
        nextTick(() => {
          if (priceChart.value) {
            debugInfo.value += ' | Canvas está disponível'
            renderizarGrafico()
          } else {
            debugInfo.value += ' | Canvas NÃO está disponível'
            // Tentar novamente após um delay
            setTimeout(() => {
              if (priceChart.value) {
                renderizarGrafico()
              }
            }, 500)
          }
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
    debugInfo.value = 'Iniciando renderização do gráfico'
    
    if (chartInstance.value) {
      chartInstance.value.destroy()
      debugInfo.value += ' | Chart anterior destruído'
    }
    
    if (!priceChart.value) {
      debugInfo.value = 'ERRO: Canvas não disponível'
      return
    }
    
    if (historicoPrecos.value.length === 0) {
      debugInfo.value = 'ERRO: Nenhum dado para renderizar'
      return
    }
    
    try {
      const ctx = priceChart.value.getContext('2d')
      
      if (!ctx) {
        debugInfo.value = 'ERRO: Contexto 2D não disponível'
        return
      }
      
      // Preparar dados para o gráfico
      const labels = historicoPrecos.value.map(item => formatDateShort(item.data))
      const precos = historicoPrecos.value.map(item => parseFloat(item.preco))
      
      debugInfo.value = `Labels: ${labels.length}, Preços: ${precos.length}`
      
      // Dados simples para teste
      const chartData = {
        labels: labels,
        datasets: [{
          label: 'Preço (R$)',
          data: precos,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1,
          pointRadius: 5
        }]
      }
      
      // Criar o gráfico
      chartInstance.value = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: false, // Desabilitar animação para debug
          elements: {
            line: {
              borderWidth: 2
            }
          },
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
            legend: {
              display: true,
              position: 'top'
            }
          }
        }
      })
      
      debugInfo.value = 'Gráfico criado com sucesso'
      
      // Verificar se o gráfico foi renderizado
      setTimeout(() => {
        if (chartInstance.value) {
          debugInfo.value += ' | Chart instance existe'
          const canvas = chartInstance.value.canvas
          if (canvas && canvas.width && canvas.height) {
            debugInfo.value += ` | Canvas: ${canvas.width}x${canvas.height}`
          } else {
            debugInfo.value += ' | Canvas sem dimensões'
          }
        }
      }, 100)
      
    } catch (error) {
      debugInfo.value = `ERRO ao criar gráfico: ${error.message}`
      console.error('Erro ao criar gráfico:', error)
    }
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
      chartInstance.value.options.plugins.title = {
        display: true,
        text: `Histórico de Preços - ${nome} (${concorrente})`
      }
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
  
  return {
    // Estado
    historicoPrecos,
    carregandoHistorico,
    priceChart,
    chartContainer,
    debugInfo,
    
    // Métodos
    carregarHistoricoCompleto,
    renderizarGrafico,
    atualizarTituloGrafico
  }
}