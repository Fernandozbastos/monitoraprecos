<template>
    <v-row>
      <v-col cols="12" md="4">
        <stat-card
          title="Total de Produtos"
          :value="stats.totalProdutos"
          icon="mdi-package-variant-closed"
          color="primary"
        />
      </v-col>
      
      <v-col cols="12" md="4">
        <stat-card
          title="Concorrentes"
          :value="stats.totalConcorrentes"
          icon="mdi-account-group"
          color="info"
        />
      </v-col>
      
      <v-col cols="12" md="4">
        <stat-card
          title="Comparações"
          :value="stats.totalComparacoes"
          icon="mdi-compare"
          color="success"
        />
      </v-col>
    </v-row>
  </template>
  
  <script setup>
  import StatCard from './StatCard.vue'
  
  defineProps({
    stats: {
      type: Object,
      required: true,
      validator: (value) => {
        return value.hasOwnProperty('totalProdutos') &&
               value.hasOwnProperty('totalConcorrentes') &&
               value.hasOwnProperty('totalComparacoes')
      }
    }
  })
  </script>