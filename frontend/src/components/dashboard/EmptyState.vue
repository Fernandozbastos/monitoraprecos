<template>
    <div class="text-center pa-8">
      <v-img
        src="@/assets/empty-products.svg"
        max-width="200"
        class="mx-auto mb-4"
        alt="Nenhum produto encontrado"
      ></v-img>
      <h3 class="text-h5 grey--text text--darken-1 mt-4">{{ title }}</h3>
      <p class="text-body-1 grey--text mb-6">{{ message }}</p>
      <v-btn
        color="primary"
        @click="$emit('action')"
        v-if="showButton"
      >
        <v-icon left>{{ buttonIcon }}</v-icon>
        {{ buttonText }}
      </v-btn>
    </div>
  </template>
  
  <script setup>
  defineProps({
    title: {
      type: String,
      default: 'Nenhum produto encontrado'
    },
    message: {
      type: String,
      default: 'Comece adicionando produtos usando o botão no topo da página'
    },
    showButton: {
      type: Boolean,
      default: true
    },
    buttonText: {
      type: String,
      default: 'Adicionar Produto'
    },
    buttonIcon: {
      type: String,
      default: 'mdi-plus'
    }
  })
  
  defineEmits(['action'])
  </script>
  
  <style scoped>
  /* Estilos específicos se necessário */
  </style>