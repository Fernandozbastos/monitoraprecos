<!-- frontend/src/components/product-list/ProductListFilters.vue -->
<template>
    <div class="d-flex align-center">
      <v-text-field
        :model-value="search"
        @update:model-value="updateSearch"
        append-icon="mdi-magnify"
        label="Pesquisar produtos..."
        single-line
        hide-details
        outlined
        dense
        clearable
        class="search-field"
      ></v-text-field>
      
      <v-spacer></v-spacer>
      
      <v-chip-group
        :model-value="selectedTypes"
        @update:model-value="updateTypes"
        multiple
        column
        class="ml-4"
      >
        <v-chip
          filter
          outlined
          color="primary"
        >
          Cliente
        </v-chip>
        <v-chip
          filter
          outlined
          color="secondary"
        >
          Concorrente
        </v-chip>
      </v-chip-group>
      
      <v-btn
        icon
        color="grey darken-1"
        class="ml-2"
        @click="clearFilters"
        v-if="hasFilters"
      >
        <v-icon>mdi-filter-remove</v-icon>
      </v-btn>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    search: {
      type: String,
      required: true
    },
    selectedTypes: {
      type: Array,
      required: true
    }
  })
  
  const emit = defineEmits(['update:search', 'update:selectedTypes', 'clear-filters'])
  
  const hasFilters = computed(() => {
    return props.search || props.selectedTypes.length > 0
  })
  
  const updateSearch = (value) => {
    emit('update:search', value)
  }
  
  const updateTypes = (value) => {
    emit('update:selectedTypes', value)
  }
  
  const clearFilters = () => {
    emit('clear-filters')
  }
  </script>
  
  <style scoped>
  .search-field {
    max-width: 400px;
  }
  
  :deep(.v-chip-group) {
    margin-right: 0 !important;
  }
  </style>