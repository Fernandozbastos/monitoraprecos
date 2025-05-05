<!-- frontend/src/components/product-list/ProductListNotFound.vue -->
<template>
    <div class="text-center py-8">
      <v-img
        src="@/assets/empty-products.svg"
        max-width="200"
        class="mx-auto mb-4"
        alt="Nenhum produto encontrado"
      ></v-img>
      <h3 class="text-h5 grey--text text--darken-1 mb-2">
        {{ hasSearch ? 'Nenhum produto corresponde à sua pesquisa' : 'Nenhum produto encontrado' }}
      </h3>
      <p class="text-body-1 grey--text mb-4">
        {{ 
          hasSearch ? 
          'Tente ajustar os filtros ou remover a pesquisa' : 
          'Comece adicionando seu primeiro produto' 
        }}
      </p>
      <v-btn
        v-if="!hasSearch"
        color="primary"
        @click="$emit('add-product')"
        class="px-8"
        elevation="2"
      >
        <v-icon left>mdi-plus</v-icon>
        Adicionar Produto
      </v-btn>
      <v-btn
        v-else
        color="primary"
        outlined
        @click="$emit('clear-search')"
        class="px-8"
      >
        <v-icon left>mdi-close</v-icon>
        Limpar Filtros
      </v-btn>
    </div>
  </template>
  
  <script setup>
  const props = defineProps({
    hasSearch: {
      type: Boolean,
      default: false
    }
  })
  
  const emit = defineEmits(['add-product', 'clear-search'])
  </script>
  
  <style scoped>
  /* O SVG de estado vazio já está no arquivo original */
  </style>