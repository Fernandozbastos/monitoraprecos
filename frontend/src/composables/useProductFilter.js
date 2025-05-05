import { ref, computed } from 'vue'

export const useProductFilter = (produtos) => {
  const search = ref('')
  const gruposAbertos = ref([])
  
  // Produtos únicos (pelo nome)
  const produtosUnicos = computed(() => {
    const nomes = new Set()
    const unicos = []
    
    produtos.value.forEach(produto => {
      if (!nomes.has(produto.nome)) {
        nomes.add(produto.nome)
        unicos.push(produto)
      }
    })
    
    return unicos
  })
  
  // Concorrentes únicos
  const concorrentesUnicos = computed(() => {
    const nomes = new Set()
    produtos.value.forEach(p => {
      if (p.tipo_produto === 'concorrente' && p.concorrente) {
        nomes.add(p.concorrente)
      }
    })
    return Array.from(nomes)
  })
  
  // Produtos agrupados por nome
  const produtosAgrupados = computed(() => {
    const grupos = []
    const nomesProdutos = new Set()
    
    // Coletar nomes únicos
    produtos.value.forEach(p => nomesProdutos.add(p.nome))
    
    // Para cada nome, criar um grupo
    Array.from(nomesProdutos).forEach(nome => {
      const produtosDesseTipo = produtos.value.filter(p => p.nome === nome)
      
      // Produto cliente base (marcado como produto_cliente)
      const produtoClienteBase = produtosDesseTipo.find(p => p.produto_cliente === true)
      
      // Produtos concorrentes
      const produtosConcorrentes = produtosDesseTipo.filter(p => p.tipo_produto === 'concorrente')
      
      // Encontrar menor preço entre concorrentes
      let menorPrecoConcorrente = null
      let concorrenteMenorPreco = null
      
      if (produtosConcorrentes.length > 0) {
        const concorrentesComPreco = produtosConcorrentes.filter(p => {
          const preco = p.preco_ultimo || p.menor_preco_concorrente
          return preco !== null && preco !== undefined && !isNaN(preco) && preco > 0
        })
        
        if (concorrentesComPreco.length > 0) {
          let menorPreco = Number.MAX_SAFE_INTEGER
          let produtoMenorPreco = null
          
          concorrentesComPreco.forEach(p => {
            const preco = p.preco_ultimo || p.menor_preco_concorrente
            if (preco < menorPreco) {
              menorPreco = preco
              produtoMenorPreco = p
            }
          })
          
          menorPrecoConcorrente = menorPreco
          concorrenteMenorPreco = produtoMenorPreco?.concorrente
        }
      }
      
      // Se não tiver produto cliente base, usar qualquer produto do cliente
      let produtoClienteExibicao = produtoClienteBase
      if (!produtoClienteExibicao) {
        produtoClienteExibicao = produtosDesseTipo.find(p => p.tipo_produto === 'cliente')
      }
      
      // Calcular diferença percentual
      let diferencaPercentual = null
      if (produtoClienteExibicao && 
          produtoClienteExibicao.preco_cliente && 
          !isNaN(produtoClienteExibicao.preco_cliente) && 
          menorPrecoConcorrente && 
          !isNaN(menorPrecoConcorrente)) {
        
        diferencaPercentual = ((produtoClienteExibicao.preco_cliente - menorPrecoConcorrente) / menorPrecoConcorrente) * 100
        diferencaPercentual = Math.round(diferencaPercentual * 10) / 10
      }
      
      // Processar cada produto para exibição na tabela
      const produtosProcessados = produtosDesseTipo.map(p => {
        let diferencaIndividual = null
        
        // Para produtos do cliente, calcular a diferença em relação ao menor preço concorrente
        if (p.tipo_produto === 'cliente' && p.preco_cliente && menorPrecoConcorrente) {
          diferencaIndividual = ((p.preco_cliente - menorPrecoConcorrente) / menorPrecoConcorrente) * 100
          diferencaIndividual = Math.round(diferencaIndividual * 10) / 10
        }
        
        // Para produtos concorrentes, calcular a diferença em relação ao produto cliente base
        if (p.tipo_produto === 'concorrente' && produtoClienteExibicao && produtoClienteExibicao.preco_cliente) {
          const precoConcorrente = p.preco_ultimo || p.menor_preco_concorrente
          if (precoConcorrente) {
            diferencaIndividual = ((precoConcorrente - produtoClienteExibicao.preco_cliente) / produtoClienteExibicao.preco_cliente) * 100
            diferencaIndividual = Math.round(diferencaIndividual * 10) / 10
          }
        }
        
        return {
          ...p,
          preco_exibicao: p.tipo_produto === 'cliente' 
            ? p.preco_cliente 
            : (p.preco_ultimo || p.menor_preco_concorrente),
          diferenca_percentual: diferencaIndividual
        }
      })
      
      grupos.push({
        nome,
        produtos: produtosProcessados,
        produtoClienteBase: produtoClienteExibicao,
        menorPrecoConcorrente,
        concorrenteMenorPreco,
        diferencaPercentual
      })
    })
    
    // Ordenar grupos pela presença de um produto cliente base primeiro
    return grupos.sort((a, b) => {
      // Priorizar grupos com produto cliente base
      if (a.produtoClienteBase && !b.produtoClienteBase) return -1
      if (!a.produtoClienteBase && b.produtoClienteBase) return 1
      // Em seguida, ordenar alfabeticamente pelo nome
      return a.nome.localeCompare(b.nome)
    })
  })
  
  // Produtos filtrados com base na pesquisa
  const produtosAgrupadosFiltrados = computed(() => {
    if (!search.value) return produtosAgrupados.value
    
    const searchTerm = search.value.toLowerCase().trim()
    
    return produtosAgrupados.value.filter(grupo => {
      // Verifica se o nome do grupo contém o termo de pesquisa
      if (grupo.nome.toLowerCase().includes(searchTerm)) return true
      
      // Verifica se algum produto deste grupo contém o termo de pesquisa
      return grupo.produtos.some(produto => 
        produto.nome.toLowerCase().includes(searchTerm) || 
        produto.concorrente.toLowerCase().includes(searchTerm)
      )
    })
  })
  
  // Função para alternar a exibição de um grupo
  const toggleGrupo = (index) => {
    const currentIndex = gruposAbertos.value.indexOf(index)
    if (currentIndex === -1) {
      gruposAbertos.value.push(index)
    } else {
      gruposAbertos.value.splice(currentIndex, 1)
    }
  }
  
  return {
    search,
    gruposAbertos,
    produtosUnicos,
    concorrentesUnicos,
    produtosAgrupados,
    produtosAgrupadosFiltrados,
    toggleGrupo
  }
}