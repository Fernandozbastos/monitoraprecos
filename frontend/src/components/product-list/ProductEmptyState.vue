<!-- frontend/src/components/product-list/ProductEmptyState.vue -->
<template>
    <div class="text-center py-8">
      <v-img
        src="@/assets/empty-products.svg"
        max-width="200"
        class="mx-auto mb-4"
        alt="Nenhum produto encontrado"
      ></v-img>
      <h3 class="text-h5 grey--text text--darken-1 mb-2">Nenhum produto cadastrado</h3>
      <p class="text-body-1 grey--text mb-6">
        Comece adicionando seu primeiro produto para monitorar
      </p>
      <v-btn
        color="primary"
        large
        @click="$emit('add-product')"
        class="px-8"
        elevation="2"
      >
        <v-icon left>mdi-plus</v-icon>
        Adicionar Produto
      </v-btn>
    </div>
  </template>
  
  <script setup>
  const emit = defineEmits(['add-product'])
  </script>
  
  <style scoped>
  .v-img {
    filter: opacity(0.7);
  }
  
  /* Animação sutil quando o estado aparece */
  .text-center {
    animation: fade-in 0.3s ease-in;
  }
  
  @keyframes fade-in {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  </style>