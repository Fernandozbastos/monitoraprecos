# frontend/src/components/dashboard/ProductGroupCard.vue (Corrigido)

```vue
<template>
  <div class="mb-5 produto-grupo">
    <!-- Cabeçalho do grupo -->
    <div 
      class="d-flex align-center pa-4 grupo-header"
      @click="handleToggle"
      :class="{'grupo-header-active': isAberto}"
    >
      <v-icon class="mr-2 transition-swing" :class="{'transform-rotate-90': isAberto}">
        mdi-chevron-right
      </v-icon>
      
      <!-- Nome do produto -->
      <span class="text-subtitle-1 font-weight-bold">{{ grupo.nome }}</span>
      
      <!-- Mensagem quando não houver produto cliente definido -->
      <v-chip
        v-if="!grupo.produtoClienteBase"
        small
        outlined
        color="warning"
        class="ml-3"
      >
        <v-icon left size="16">mdi-alert-circle</v-icon>
        Por favor, defina o produto cliente
      </v-chip>
      
      <v-spacer></v-spacer>
      
      <!-- Botão para ver histórico de preços deste grupo -->
      <v-btn
        small
        outlined
        color="primary"
        class="mr-2"
        @click.stop="$emit('open-chart', grupo)"
      >
        <v-icon left small>mdi-chart-line</v-icon>
        Ver Histórico
      </v-btn>
      
      <!-- Resumo do produto (apenas se houver produto cliente base) -->
      <group-summary
        v-if="grupo.produtoClienteBase"
        :grupo="grupo"
      />
    </div>
    
    <!-- Conteúdo do grupo (tabela de produtos) -->
    <div v-if="isAberto" class="pa-4 grupo-content">
      <product-table
        :produtos="grupo.produtos"
        :get-preco="getPreco"
        :verificando-item="verificandoItem"
        @view-details="$emit('view-details', $event)"
        @verify-price="$emit('verify-price', $event)"
        @set-base="$emit('set-base', $event)"
        @delete="$emit('delete', $event)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import ProductTable from './ProductTable.vue'
import GroupSummary from './GroupSummary.vue'

const props = defineProps({
  grupo: {
    type: Object,
    required: true
  },
  getPreco: {
    type: Function,
    required: true
  },
  verificandoItem: {
    type: [String, Number, null],
    default: null
  },
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['toggle', 'open-chart', 'view-details', 'verify-price', 'set-base', 'delete'])

const isAberto = ref(props.isOpen)

watch(() => props.isOpen, (newVal) => {
  isAberto.value = newVal
})

const handleToggle = () => {
  isAberto.value = !isAberto.value
  emit('toggle', isAberto.value)
}
</script>

<style scoped>
.produto-grupo {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.12);
  transition: box-shadow 0.3s ease;
}

.produto-grupo:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.grupo-header {
  background-color: #f5f5f5;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  transition: background-color 0.2s ease;
  cursor: pointer;
}

.grupo-header:hover {
  background-color: #eeeeee;
}

.grupo-header-active {
  background-color: #e3f2fd;
}

.grupo-content {
  background-color: white;
}

.transform-rotate-90 {
  transform: rotate(90deg);
}

.transition-swing {
  transition: transform 0.3s ease;
}
</style>
```