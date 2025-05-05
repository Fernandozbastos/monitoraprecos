import { ref, nextTick, onUnmounted, computed } from 'vue'
import Chart from 'chart.js/auto'
import 'chartjs-adapter-date-fns'
import api from '@/services/api'

export const usePriceChart = () => {
  // Estado
  const mostrarGraficoComparativo = ref(false)
  const carregandoHistoricoComparativo = ref(false)
  const chartComparativo = ref(null)
  const chartInstanceComparativo = ref(null)
  const chartContainerComparativo = ref(null)
  const dadosHistoricoComparativo = ref([])
  const grupoSelecionado = ref(null)
  
  // Filtros para o gráfico
  const tiposProdutoFiltro = ref([
    { title: 'Todos os produtos', value: 'todos' },
    { title: 'Produtos do Cliente', value: 'cliente' },
    { title: 'Produtos de Concorrentes', value: 'concorrente' }
  ])
  
  const periodosFiltro = ref([
    { title: 'Últimos 30 dias', value: '30' },
    { title: 'Últimos 60 dias', value: '60' },
    { title: 'Últimos 90 dias', value: '90' },
    { title: 'Tudo', value: 'all' }
  ])
  
  const filtroGrafico = ref({
    tipoProduto: 'todos',
    produtosIds: [],
    periodo: '30'
  })
  
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
  
  // Função para obter produtos filtrados para o dropdown
  const getProdutosParaFiltro = (produtos) => {
    let produtosFiltradosPorTipo = produtos
    
    if (filtroGrafico.value.tipoProduto !== 'todos') {
      produtosFiltradosPorTipo = produtos.filter(p => {
        return p.tipo_produto === filtroGrafico.value.tipoProduto
      })
    }
    
    return produtosFiltradosPorTipo.map(p => ({
      id: p.id,
      nome_completo: `${p.nome} (${p.concorrente})`,
      nome: p.nome,
      concorrente: p.concorrente,
      tipo_produto: p.tipo_produto
    }))
  }
  
  // Abrir modal do gráfico para um grupo
  const abrirGraficoGrupo = (grupo) => {
    grupoSelecionado.value = grupo
    const produtosDoGrupo = grupo.produtos.map(p => p.id)
    filtroGrafico.value.produtosIds = produtosDoGrupo
    mostrarGraficoComparativo.value = true
    carregarHistoricoComparativo()
  }
  
  // Abrir modal do gráfico geral
  const abrirGraficoComparativo = (produtos) => {
    grupoSelecionado.value = null
    mostrarGraficoComparativo.value = true
    
    nextTick(() => {
      if (!filtroGrafico.value.produtosIds.length && produtos?.length > 0) {
        const primeirosProdutos = produtos.slice(0, 3).map(p => p.id)
        filtroGrafico.value.produtosIds = primeirosProdutos
      }
      carregarHistoricoComparativo()
    })
  }
  
  // Fechar modal
  const fecharGraficoComparativo = () => {
    grupoSelecionado.value = null
    mostrarGraficoComparativo.value = false
    if (chartInstanceComparativo.value) {
      chartInstanceComparativo.value.destroy()
      chartInstanceComparativo.value = null
    }
  }
  
  // Atualizar gráfico
  const atualizarGraficoComparativo = () => {
    carregarHistoricoComparativo()
  }
  
  // Callback quando filtros mudam
  const onFiltroChanged = () => {
    if (filtroGrafico.value.tipoProduto !== 'todos') {
      filtroGrafico.value.produtosIds = []
    }
    carregarHistoricoComparativo()
  }
  
  // Carregar histórico de preços
  const carregarHistoricoComparativo = async () => {
    if (!filtroGrafico.value.produtosIds.length) {
      dadosHistoricoComparativo.value = []
      return
    }
    
    carregandoHistoricoComparativo.value = true
    
    try {
      const todosHistoricos = []
      
      for (const produtoId of filtroGrafico.value.produtosIds) {
        const historicoResponse = await api.get(`/produtos/${produtoId}/historico/?limit=100`)
        
        if (Array.isArray(historicoResponse.data) && historicoResponse.data.length > 0) {
          let dadosFiltrados = [...historicoResponse.data]
          
          if (filtroGrafico.value.periodo !== 'all') {
            const dias = parseInt(filtroGrafico.value.periodo)
            const dataLimite = new Date()
            dataLimite.setDate(dataLimite.getDate() - dias)
            
            dadosFiltrados = dadosFiltrados.filter(item => {
              const dataItem = new Date(item.data)
              return dataItem >= dataLimite
            })
          }
          
          if (dadosFiltrados.length > 0) {
            const dadosOrdenados = dadosFiltrados.sort(
              (a, b) => new Date(a.data) - new Date(b.data)
            )
            
            // Buscar informações do produto
            const produtoResponse = await api.get(`/produtos/${produtoId}/`)
            const produtoInfo = produtoResponse.data
            
            const historicoProcessado = {
              produtoId: produtoId,
              nome: produtoInfo.nome,
              concorrente: produtoInfo.concorrente,
              tipo_produto: produtoInfo.tipo_produto,
              dados: dadosOrdenados
            }
            
            todosHistoricos.push(historicoProcessado)
          }
        }
      }
      
      dadosHistoricoComparativo.value = todosHistoricos
      
      if (todosHistoricos.length > 0) {
        nextTick(() => {
          renderizarGraficoComparativo()
        })
      }
      
    } catch (error) {
      console.error('Erro ao carregar histórico para o gráfico comparativo:', error)
    } finally {
      carregandoHistoricoComparativo.value = false
    }
  }
  
  // Renderizar gráfico
  const renderizarGraficoComparativo = () => {
    if (chartInstanceComparativo.value) {
      chartInstanceComparativo.value.destroy()
    }
    
    if (!chartComparativo.value || dadosHistoricoComparativo.value.length === 0) return
    
    const ctx = chartComparativo.value.getContext('2d')
    
    const datasets = dadosHistoricoComparativo.value.map((histórico, index) => {
      const cor = cores[index % cores.length]
      
      const dados = histórico.dados.map(item => ({
        x: new Date(item.data),
        y: parseFloat(item.preco)
      }))
      
      return {
        label: `${histórico.nome} (${histórico.concorrente})`,
        data: dados,
        borderColor: cor,
        backgroundColor: cor.replace('1)', '0.1)'),
        borderWidth: 2,
        pointRadius: 3,
        pointBackgroundColor: cor,
        pointBorderColor: '#fff',
        pointHoverRadius: 5,
        tension: 0.3,
        fill: false
      }
    })
    
    chartInstanceComparativo.value = new Chart(ctx, {
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
              padding: 10
            }
          },
          title: {
            display: true,
            text: grupoSelecionado.value ? 
              `Histórico de Preços - ${grupoSelecionado.value.nome}` : 
              'Gráfico Comparativo de Preços',
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
  
  // Cleanup quando destruído
  onUnmounted(() => {
    if (chartInstanceComparativo.value) {
      chartInstanceComparativo.value.destroy()
      chartInstanceComparativo.value = null
    }
  })
  
  return {
    // Estado
    mostrarGraficoComparativo,
    carregandoHistoricoComparativo,
    chartComparativo,
    chartContainerComparativo,
    grupoSelecionado,
    dadosHistoricoComparativo,
    
    // Filtros
    tiposProdutoFiltro,
    periodosFiltro,
    filtroGrafico,
    
    // Funções
    abrirGraficoGrupo,
    abrirGraficoComparativo,
    fecharGraficoComparativo,
    atualizarGraficoComparativo,
    onFiltroChanged,
    carregarHistoricoComparativo,
    getProdutosParaFiltro
  }
}