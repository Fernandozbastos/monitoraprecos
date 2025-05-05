<!-- frontend/src/views/ProductList.vue -->
<template>
    <v-container fluid>
      <!-- Cabeçalho com visual melhorado -->
      <product-list-header
        :loading="loading"
        @refresh="carregarProdutos"
        @add-product="$router.push('/products/add')"
      />
      
      <!-- Filtros de busca e tipo -->
      <v-card elevation="2" class="mb-4">
        <v-card-title>
          <product-list-filters
            v-model:search="search"
            v-model:selected-types="selectedTypes"
            @clear-filters="clearFilters"
          />
        </v-card-title>
        
        <!-- Tabela de produtos ou estado vazio -->
        <v-card-text>
          <!-- Estado vazio quando não há produtos -->
          <product-empty-state
            v-if="produtos.length === 0 && !loading"
            @add-product="$router.push('/products/add')"
          />
          
          <!-- Tabela de produtos -->
          <product-table
            v-else-if="produtosFiltrados.length > 0 || search || selectedTypes.length > 0"
            :headers="headers"
            :produtos="produtosFiltrados"
            :loading="loading"
            :search="search"
            :verificando-item="verificandoItem"
            :format-url="formatUrl"
            :format-date="formatDate"
            :get-verification-status-color="getVerificationStatusColor"
            :get-verification-status-icon="getVerificationStatusIcon"
            @view-details="verDetalhes"
            @verify-price="verificarPreco"
            @edit-product="editarProduto"
          />
          
          <!-- Estado quando a busca não encontra resultados -->
          <product-list-not-found
            v-else
            :has-search="!!(search || selectedTypes.length > 0)"
            @add-product="$router.push('/products/add')"
            @clear-search="clearFilters"
          />
        </v-card-text>
      </v-card>
      
      <!-- Snackbar para notificações -->
      <custom-snackbar />
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useProductList } from '@/composables/useProductList'
  
  // Componentes
  import ProductListHeader from '@/components/product-list/ProductListHeader.vue'
  import ProductListFilters from '@/components/product-list/ProductListFilters.vue'
  import ProductTable from '@/components/product-list/ProductTable.vue'
  import ProductEmptyState from '@/components/product-list/ProductEmptyState.vue'
  import ProductListNotFound from '@/components/product-list/ProductListNotFound.vue'
  import CustomSnackbar from '@/components/common/CustomSnackbar.vue'
  
  const router = useRouter()
  
  // Usar o composable
  const {
    loading,
    produtos,
    search,
    verificandoItem,
    selectedTypes,
    headers,
    produtosFiltrados,
    carregarProdutos,
    formatUrl,
    formatDate,
    getVerificationStatusColor,
    getVerificationStatusIcon,
    verDetalhes,
    verificarPreco
  } = useProductList()
  
  // Métodos adicionais
  const editarProduto = (id) => {
    router.push(`/products/${id}/edit`)
  }
  
  const clearFilters = () => {
    search.value = ''
    selectedTypes.value = []
  }
  
  // Lifecycle hook
  onMounted(() => {
    carregarProdutos()
  })
  </script>
  
  <style scoped>
  /* Estilos globais foram movidos para os componentes individuais */
  </style>