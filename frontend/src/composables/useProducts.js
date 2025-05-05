import { ref } from 'vue'
import { useStore } from 'vuex'
import api from '@/services/api'

export const useProducts = () => {
  const store = useStore()
  const loading = ref(false)
  const produtos = ref([])
  const verificandoItem = ref(null)
  
  // Função para obter o preço do produto (cliente ou concorrente)
  const getPreco = (produto) => {
    if (produto.tipo_produto === 'cliente') {
      // Verificar se preco_cliente existe e é válido
      if (produto.preco_cliente !== null && produto.preco_cliente !== undefined && 
          !isNaN(produto.preco_cliente) && produto.preco_cliente > 0) {
        return produto.preco_cliente
      }
      
      // Caso não tenha, verificar preco_ultimo
      if (produto.preco_ultimo !== null && produto.preco_ultimo !== undefined && 
          !isNaN(produto.preco_ultimo) && produto.preco_ultimo > 0) {
        return produto.preco_ultimo
      }
      
      return null
    } else {
      // Para produtos concorrentes, verificar preco_ultimo (do histórico)
      if (produto.preco_ultimo !== null && produto.preco_ultimo !== undefined && 
          !isNaN(produto.preco_ultimo) && produto.preco_ultimo > 0) {
        return produto.preco_ultimo
      }
      
      // Verificar menor_preco_concorrente
      if (produto.menor_preco_concorrente !== null && produto.menor_preco_concorrente !== undefined && 
          !isNaN(produto.menor_preco_concorrente) && produto.menor_preco_concorrente > 0) {
        return produto.menor_preco_concorrente
      }
      
      return null
    }
  }
  
  // Carregar dados de produtos
  const carregarDados = async () => {
    loading.value = true
    try {
      produtos.value = []
      const timestamp = new Date().getTime()
      const produtosResponse = await api.get(`/produtos/?t=${timestamp}`)
      
      if (produtosResponse.data.results && Array.isArray(produtosResponse.data.results)) {
        produtos.value = produtosResponse.data.results
        
        // Para cada produto, recuperar o histórico de preços
        const produtosPromises = produtos.value.map(async (produto) => {
          try {
            const historicoResponse = await api.get(`/historico/?produto=${produto.id}&limit=1`)
            
            if (historicoResponse.data?.results?.length > 0) {
              const precoHistorico = parseFloat(historicoResponse.data.results[0].preco)
              produto.preco_ultimo = precoHistorico
              
              // Para produtos do cliente sem preço, usar o do histórico
              if (produto.tipo_produto === 'cliente' && (!produto.preco_cliente || produto.preco_cliente === 0)) {
                produto.preco_cliente = precoHistorico
                
                // Atualizar no backend
                try {
                  await api.patch(`/produtos/${produto.id}/`, {
                    preco_cliente: precoHistorico,
                    cliente: produto.cliente,
                    grupo: produto.grupo
                  })
                } catch (err) {
                  console.error(`Erro ao atualizar preço no backend:`, err)
                }
              }
            }
          } catch (error) {
            console.error(`Erro ao carregar histórico do produto ${produto.id}:`, error)
          }
        })
        
        await Promise.all(produtosPromises)
      }
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
      throw error
    } finally {
      loading.value = false
    }
  }
  
  // Verificar preço de um produto
  const verificarPreco = async (produtoId) => {
    verificandoItem.value = produtoId
    try {
      await api.post(`/produtos/${produtoId}/verificar/`)
      await carregarDados()
      return true
    } catch (error) {
      console.error('Erro ao verificar preço:', error)
      throw error
    } finally {
      verificandoItem.value = null
    }
  }
  
  // Definir um produto como cliente base
  const definirProdutoClienteBase = async (produto) => {
    if (!store.getters['auth/user']?.cliente_atual) {
      throw new Error('Por favor, selecione um cliente atual no menu superior antes de continuar')
    }
    
    // Obter o ID do cliente atual
    const clienteId = typeof store.getters['auth/user'].cliente_atual === 'object' 
      ? store.getters['auth/user'].cliente_atual.id 
      : store.getters['auth/user'].cliente_atual
    
    const grupoId = typeof produto.grupo === 'object' 
      ? produto.grupo.id 
      : produto.grupo
    
    // Encontrar TODOS os produtos com o mesmo nome que não são o atual
    const outrosProdutos = produtos.value.filter(p => 
      p.nome === produto.nome && 
      p.id !== produto.id
    )
    
    // Se houver algum produto que está marcado como produto_cliente, desmarcá-lo
    const produtosMarcadosComoBase = outrosProdutos.filter(p => p.produto_cliente === true)
    
    if (produtosMarcadosComoBase.length > 0) {
      for (const produtoAnterior of produtosMarcadosComoBase) {
        try {
          await api.patch(`/produtos/${produtoAnterior.id}/`, {
            produto_cliente: false,
            tipo_produto: 'concorrente',
            cliente: clienteId,
            grupo: grupoId
          })
          
          // Atualizar localmente
          const idx = produtos.value.findIndex(p => p.id === produtoAnterior.id)
          if (idx !== -1) {
            produtos.value[idx].produto_cliente = false
            produtos.value[idx].tipo_produto = 'concorrente'
          }
        } catch (err) {
          console.error(`Erro ao desmarcar produto ${produtoAnterior.id}:`, err)
        }
      }
    }
    
    // Garantir que TODOS os outros produtos com o mesmo nome sejam marcados como concorrentes
    for (const outroProduto of outrosProdutos) {
      if (outroProduto.tipo_produto !== 'concorrente') {
        try {
          await api.patch(`/produtos/${outroProduto.id}/`, {
            tipo_produto: 'concorrente',
            produto_cliente: false,
            cliente: clienteId,
            grupo: grupoId
          })
          
          // Atualizar localmente
          const idx = produtos.value.findIndex(p => p.id === outroProduto.id)
          if (idx !== -1) {
            produtos.value[idx].tipo_produto = 'concorrente'
            produtos.value[idx].produto_cliente = false
          }
        } catch (err) {
          console.error(`Erro ao alterar tipo do produto ${outroProduto.id}:`, err)
        }
      }
    }
    
    // Finalmente, atualizar o produto selecionado como cliente base
    const dadosAtualizacao = {
      produto_cliente: true,
      tipo_produto: 'cliente',
      cliente: clienteId,
      grupo: grupoId,
    }
    
    await api.patch(`/produtos/${produto.id}/`, dadosAtualizacao)
    
    // Atualizar localmente
    const produtoIndex = produtos.value.findIndex(p => p.id === produto.id)
    if (produtoIndex !== -1) {
      produtos.value[produtoIndex].produto_cliente = true
      produtos.value[produtoIndex].tipo_produto = 'cliente'
    }
    
    // Recarregar dados após a atualização
    await carregarDados()
  }
  
  // Excluir um produto
  const excluirProduto = async (produto) => {
    if (!store.getters['auth/user']?.cliente_atual) {
      throw new Error('Por favor, selecione um cliente atual no menu superior antes de continuar')
    }
    
    // Verificar se é um produto cliente base
    const ehProdutoClienteBase = produto.produto_cliente === true
    
    // Excluir o produto
    await api.delete(`/produtos/${produto.id}/`)
    
    // Se era um produto cliente base, verificar se há outros produtos do mesmo nome
    if (ehProdutoClienteBase) {
      const outrosProdutos = produtos.value.filter(p => 
        p.nome === produto.nome && 
        p.id !== produto.id
      )
      
      if (outrosProdutos.length > 0) {
        console.log(`O produto cliente base foi excluído. Existem ${outrosProdutos.length} outros produtos com o mesmo nome.`)
      }
    }
    
    // Remover o produto da lista local
    const produtoIndex = produtos.value.findIndex(p => p.id === produto.id)
    if (produtoIndex !== -1) {
      produtos.value.splice(produtoIndex, 1)
    }
    
    // Recarregar dados após a exclusão
    await carregarDados()
  }
  
  return {
    loading,
    produtos,
    verificandoItem,
    carregarDados,
    verificarPreco,
    definirProdutoClienteBase,
    excluirProduto,
    getPreco
  }
}