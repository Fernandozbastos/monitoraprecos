// frontend/src/composables/useProductList.js

import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import { useSnackbar } from '@/composables/useSnackbar'

export const useProductList = () => {
  const router = useRouter()
  const { mostrarSnackbar } = useSnackbar()
  
  // Estado
  const loading = ref(false)
  const produtos = ref([])
  const search = ref('')
  const verificandoItem = ref(null)
  const selectedTypes = ref([]) // Filtro por tipo de produto
  
  // Headers da tabela
  const headers = [
    { text: 'Tipo', value: 'tipo_produto', width: '100px', align: 'center' },
    { text: 'Nome', value: 'nome' },
    { text: 'Concorrente', value: 'concorrente' },
    { text: 'Plataforma', value: 'plataforma_nome', width: '150px' },
    { text: 'URL', value: 'url' },
    { text: 'Verificação', value: 'verificacao_manual', width: '100px', align: 'center' },
    { text: 'Última Verificação', value: 'ultima_verificacao', width: '200px' },
    { text: 'Ações', value: 'actions', sortable: false, align: 'center', width: '150px' }
  ]
  
  // Produtos filtrados por tipo (cliente/concorrente)
  const produtosFiltrados = computed(() => {
    if (selectedTypes.value.length === 0) {
      return produtos.value
    }
    
    // Mapear seleção para tipos reais
    const tiposFiltrados = []
    if (selectedTypes.value.includes(0)) tiposFiltrados.push('cliente')
    if (selectedTypes.value.includes(1)) tiposFiltrados.push('concorrente')
    
    return produtos.value.filter(produto => tiposFiltrados.includes(produto.tipo_produto))
  })
  
  // Carregar produtos
  const carregarProdutos = async () => {
    loading.value = true
    try {
      // Prevenir cache adicionando timestamp
      const timestamp = new Date().getTime()
      const response = await api.get(`/produtos/?t=${timestamp}`)
      
      if (response.data.results && Array.isArray(response.data.results)) {
        produtos.value = response.data.results
      } else {
        produtos.value = []
      }
    } catch (error) {
      console.error('Erro ao carregar produtos:', error)
      mostrarSnackbar('Erro ao carregar produtos', 'error')
    } finally {
      loading.value = false
    }
  }
  
  // Formatar URL para exibição compacta
  const formatUrl = (url) => {
    if (!url) return '';
    try {
      // Remover protocolo e www
      let formatted = url.replace(/^https?:\/\//i, '').replace(/^www\./i, '')
      // Limitar tamanho
      if (formatted.length > 30) {
        formatted = formatted.substring(0, 30) + '...'
      }
      return formatted
    } catch (e) {
      return url
    }
  }
  
  // Formatar data de verificação
  const formatDate = (dateString) => {
    if (!dateString) return 'Nunca verificado'
    try {
      const options = { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }
      return new Date(dateString).toLocaleString('pt-BR', options)
    } catch (error) {
      return dateString || 'Data inválida'
    }
  }
  
  // Obter cor para status de verificação
  const getVerificationStatusColor = (date) => {
    if (!date) return 'grey'
    
    const now = new Date()
    const verificationDate = new Date(date)
    const diffHours = (now - verificationDate) / (1000 * 60 * 60)
    
    if (diffHours < 24) return 'success'
    if (diffHours < 72) return 'warning'
    return 'error'
  }
  
  // Obter ícone para status de verificação
  const getVerificationStatusIcon = (date) => {
    if (!date) return 'mdi-alert-circle-outline'
    
    const now = new Date()
    const verificationDate = new Date(date)
    const diffHours = (now - verificationDate) / (1000 * 60 * 60)
    
    if (diffHours < 24) return 'mdi-check-circle-outline'
    if (diffHours < 72) return 'mdi-clock-alert-outline'
    return 'mdi-alert-circle-outline'
  }
  
  // Navegar para detalhes do produto
  const verDetalhes = (id) => {
    router.push(`/products/${id}`)
  }
  
  // Verificar preço do produto
  const verificarPreco = async (id) => {
    verificandoItem.value = id
    try {
      await api.post(`/produtos/${id}/verificar/`)
      // Recarregar dados após verificação
      await carregarProdutos()
      mostrarSnackbar('Preço verificado com sucesso', 'success')
    } catch (error) {
      console.error('Erro ao verificar preço:', error)
      mostrarSnackbar('Erro ao verificar preço', 'error')
    } finally {
      verificandoItem.value = null
    }
  }
  
  return {
    // Estado
    loading,
    produtos,
    search,
    verificandoItem,
    selectedTypes,
    headers,
    
    // Computed
    produtosFiltrados,
    
    // Métodos
    carregarProdutos,
    formatUrl,
    formatDate,
    getVerificationStatusColor,
    getVerificationStatusIcon,
    verDetalhes,
    verificarPreco
  }
}