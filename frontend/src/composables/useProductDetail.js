// frontend/src/composables/useProductDetail.js

import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import api from '@/services/api'
import { useSnackbar } from '@/composables/useSnackbar'

export const useProductDetail = () => {
  const route = useRoute()
  const router = useRouter()
  const store = useStore()
  const { mostrarSnackbar } = useSnackbar()
  
  // Estado do produto
  const loading = ref(true)
  const produto = ref({})
  const precoCliente = ref(0)
  const formValid = ref(false)
  const form = ref(null)
  
  // Estados das ações
  const verificando = ref(false)
  const atualizandoPreco = ref(false)
  const atualizandoStatus = ref(false)
  const corrigindoTipo = ref(false)
  
  // Regras de validação
  const precoRules = [
    v => !!v || 'O preço é obrigatório',
    v => v > 0 || 'O preço deve ser maior que zero'
  ]
  
  // Formatação de data
  const formatDate = (dateString) => {
    if (!dateString) return 'Nunca'
    const options = { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }
    try {
      return new Date(dateString).toLocaleString('pt-BR', options)
    } catch (e) {
      console.error('Erro ao formatar data:', e)
      return dateString
    }
  }
  
  // Formatação de preço
  const formatarPreco = (valor) => {
    if (valor === null || valor === undefined) return 'N/A'
    return `R$ ${Number(valor).toFixed(2).replace('.', ',')}`
  }
  
  // Formatação de percentual
  const formatarPercentual = (valor) => {
    if (valor === null || valor === undefined) return 'N/A'
    const sinal = valor > 0 ? '+' : ''
    return `${sinal}${valor.toFixed(1).replace('.', ',')}%`
  }
  
  // Verificar preço manualmente
  const verificarPreco = async () => {
    if (!produto.value.id) {
      console.error('ID do produto não disponível')
      return
    }
    
    verificando.value = true
    try {
      await api.post(`/produtos/${produto.value.id}/verificar/`)
      await carregarProduto()
      mostrarSnackbar('Preço verificado com sucesso')
    } catch (error) {
      console.error('Erro ao verificar preço:', error)
      mostrarSnackbar('Erro ao verificar preço', 'error')
    } finally {
      verificando.value = false
    }
  }
  
  // Atualizar preço do cliente
  const atualizarPrecoCliente = async () => {
    if (!produto.value.id || produto.value.tipo_produto !== 'cliente') {
      console.error('Operação não permitida')
      return
    }
    
    atualizandoPreco.value = true
    try {
      await api.post(`/produtos/${produto.value.id}/atualizar_preco_cliente/`, {
        preco_cliente: precoCliente.value
      })
      
      await carregarProduto()
      mostrarSnackbar('Preço atualizado com sucesso')
    } catch (error) {
      console.error('Erro ao atualizar preço do cliente:', error)
      mostrarSnackbar('Erro ao atualizar preço do cliente', 'error')
    } finally {
      atualizandoPreco.value = false
    }
  }
  
  // Atualizar status de produto cliente
  const atualizarProdutoClienteStatus = async () => {
    atualizandoStatus.value = true
    try {
      const userInfo = await api.get('/user/info/')
      if (!userInfo.data.cliente_atual) {
        mostrarSnackbar('Por favor, selecione um cliente atual antes de continuar', 'warning')
        return
      }
      
      const clienteId = typeof userInfo.data.cliente_atual === 'object' 
        ? userInfo.data.cliente_atual.id 
        : userInfo.data.cliente_atual
      
      const grupoId = typeof produto.value.grupo === 'object' 
        ? produto.value.grupo.id 
        : produto.value.grupo
      
      const dadosAtualizacao = {
        produto_cliente: produto.value.produto_cliente,
        cliente: clienteId,
        grupo: grupoId
      }
      
      if (produto.value.produto_cliente) {
        if (produto.value.tipo_produto === 'concorrente') {
          dadosAtualizacao.tipo_produto = 'cliente'
          produto.value.tipo_produto = 'cliente'
        }
        
        // Desmarcar outros produtos com o mesmo nome
        try {
          const produtosResponse = await api.get(`/produtos/?nome=${produto.value.nome}`)
          const produtosDoMesmoNome = produtosResponse.data.results.filter(p => 
            p.id !== produto.value.id && 
            p.produto_cliente === true && 
            p.nome === produto.value.nome
          )
          
          for (const produtoAnterior of produtosDoMesmoNome) {
            await api.patch(`/produtos/${produtoAnterior.id}/`, {
              produto_cliente: false,
              cliente: clienteId,
              grupo: grupoId
            })
          }
        } catch (err) {
          console.error('Erro ao verificar outros produtos marcados como base:', err)
        }
      }
      
      await api.patch(`/produtos/${produto.value.id}/`, dadosAtualizacao)
      
      if (produto.value.produto_cliente) {
        mostrarSnackbar('Produto definido como produto cliente base', 'success')
        if (dadosAtualizacao.tipo_produto) {
          await carregarProduto()
        }
      } else {
        mostrarSnackbar('Produto removido como produto cliente base', 'success')
      }
      
    } catch (error) {
      console.error('Erro ao atualizar status de produto cliente:', error)
      produto.value.produto_cliente = !produto.value.produto_cliente
      if (produto.value.tipo_produto === 'cliente' && !produto.value.produto_cliente) {
        produto.value.tipo_produto = 'concorrente'
      }
      mostrarSnackbar('Erro ao atualizar status de produto cliente: ' + 
        (error.response?.data?.detail || error.message), 'error')
    } finally {
      atualizandoStatus.value = false
    }
  }
  
  // Corrigir tipo do produto
  const corrigirTipoProduto = async () => {
    corrigindoTipo.value = true
    try {
      await api.patch(`/produtos/${produto.value.id}/`, {
        tipo_produto: 'cliente'
      })
      
      produto.value.tipo_produto = 'cliente'
      mostrarSnackbar('Tipo do produto corrigido para Cliente', 'success')
      await carregarProduto()
    } catch (error) {
      console.error('Erro ao corrigir tipo do produto:', error)
      mostrarSnackbar('Erro ao corrigir tipo do produto', 'error')
    } finally {
      corrigindoTipo.value = false
    }
  }
  
  // Excluir produto
  const excluirProduto = async () => {
    if (!produto.value.id) {
      console.error('ID do produto não disponível')
      return
    }
    
    if (!confirm(`Tem certeza que deseja excluir o produto "${produto.value.nome}"?`)) {
      return
    }
    
    try {
      await api.delete(`/produtos/${produto.value.id}/`)
      mostrarSnackbar('Produto excluído com sucesso')
      router.push('/products')
    } catch (error) {
      console.error('Erro ao excluir produto:', error)
      
      if (error.response) {
        console.error('Detalhes do erro:', error.response.data)
        
        if (error.response.status === 403) {
          mostrarSnackbar('Você não tem permissão para excluir este produto.', 'error')
        } else {
          mostrarSnackbar(`Erro ao excluir produto: ${error.response.data.detail || 'Erro interno do servidor'}`, 'error')
        }
      } else {
        mostrarSnackbar('Erro de conexão ao tentar excluir o produto', 'error')
      }
    }
  }
  
  // Carregar informações do produto
  const carregarProduto = async () => {
    loading.value = true
    try {
      const produtoId = route.params.id
      const response = await api.get(`/produtos/${produtoId}/`)
      produto.value = response.data
      
      if (produto.value.produto_cliente && produto.value.tipo_produto === 'concorrente') {
        console.warn('Inconsistência: Produto marcado como produto_cliente, mas é do tipo concorrente:', produto.value)
        mostrarSnackbar('Este produto está marcado como produto cliente base, mas é do tipo concorrente. Considere ajustar o tipo.', 'warning', 6000)
      }
      
      if (produto.value.tipo_produto === 'cliente') {
        if (produto.value.preco_cliente !== null && produto.value.preco_cliente !== undefined) {
          precoCliente.value = produto.value.preco_cliente
        } else {
          precoCliente.value = 0
          produto.value.preco_cliente = 0
        }
      }
      
      try {
        const historicoResponse = await api.get(`/historico/?produto=${produtoId}&limit=1`)
        if (historicoResponse.data.results && historicoResponse.data.results.length > 0) {
          const precoMaisRecente = parseFloat(historicoResponse.data.results[0].preco)
          
          if (produto.value.tipo_produto === 'cliente' && 
              (produto.value.preco_cliente === null || produto.value.preco_cliente === undefined || produto.value.preco_cliente === 0)) {
            produto.value.preco_cliente = precoMaisRecente
            precoCliente.value = precoMaisRecente
          }
          
          if (produto.value.tipo_produto === 'concorrente' && produto.value.produto_cliente) {
            produto.value.preco_exibicao = precoMaisRecente
          }
        }
      } catch (error) {
        console.error('Erro ao carregar histórico de preços:', error)
      }
      
    } catch (error) {
      console.error('Erro ao carregar produto:', error)
      produto.value = {}
      mostrarSnackbar('Erro ao carregar produto', 'error')
    } finally {
      loading.value = false
    }
  }
  
  // Lifecycle hooks
  onMounted(() => {
    carregarProduto()
  })
  
  watch(() => route.params.id, (newId, oldId) => {
    if (newId !== oldId) {
      carregarProduto()
    }
  })
  
  return {
    // Estado
    loading,
    produto,
    precoCliente,
    formValid,
    form,
    verificando,
    atualizandoPreco,
    atualizandoStatus,
    corrigindoTipo,
    
    // Regras
    precoRules,
    
    // Métodos
    formatDate,
    formatarPreco,
    formatarPercentual,
    verificarPreco,
    atualizarPrecoCliente,
    atualizarProdutoClienteStatus,
    corrigirTipoProduto,
    excluirProduto,
    carregarProduto
  }
}