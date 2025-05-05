# frontend/src/components/dashboard/ComparativeChartModal.vue (Corrigido)

```vue
<template>
  <v-dialog
    v-model="mostrarGrafico"
    max-width="1200px"
    persistent
  >
    <v-card>
      <v-card-title class="primary white--text">
        <span v-if="grupoSelecionado">
          Histórico de Preços - {{ grupoSelecionado.nome }}
        </span>
        <span v-else>
          Gráfico Comparativo de Preços
        </span>
        <v-spacer></v-spacer>
        <v-btn
          icon
          color="white"
          @click="fechaModal"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      
      <v-card-text class="pa-6">
        <!-- Opções de filtro para o gráfico -->
        <v-row>
          <v-col cols="12" sm="4">
            <v-select
              v-model="filtroGrafico.tipoProduto"
              :items="tiposProdutoFiltro"
              item-title="title"
              item-value="value"
              label="Tipo de Produtos"
              outlined
              dense
              hide-details
              class="mb-4"
              @update:modelValue="$emit('filtro-changed')"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="4">
            <v-select
              v-model="filtroGrafico.produtosIds"
              :items="produtosParaFiltro"
              item-title="nome_completo"
              item-value="id"
              label="Produtos"
              outlined
              dense
              hide-details
              class="mb-4"
              multiple
              chips
              closable-chips
              @update:modelValue="$emit('filtro-changed')"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="4">
            <v-select
              v-model="filtroGrafico.periodo"
              :items="periodosFiltro"
              item-title="title"
              item-value="value"
              label="Período"
              outlined
              dense
              hide-details
              class="mb-4"
              @update:modelValue="$emit('filtro-changed')"
            ></v-select>
          </v-col>
        </v-row>
        
        <!-- Conteúdo do gráfico -->
        <div v-if="carregandoHistoricoComparativo" class="d-flex justify-center align-center py-12">
          <v-progress-circular indeterminate size="64" color="primary"></v-progress-circular>
          <span class="ml-4 text-subtitle-1">Carregando dados de histórico...</span>
        </div>
        
        <div v-else-if="!dadosHistoricoComparativo || !dadosHistoricoComparativo.length" class="text-center py-12">
          <v-icon size="64" color="grey lighten-1">mdi-chart-timeline-variant</v-icon>
          <h3 class="text-h6 grey--text text--darken-1 mt-4">Nenhum dado histórico encontrado</h3>
          <p class="text-body-2 grey--text mb-4">Selecione um ou mais produtos para visualizar o histórico</p>
        </div>
        
        <div v-else ref="chartContainer" style="height: 500px; width: 100%;">
          <canvas ref="chart"></canvas>
        </div>
      </v-card-text>
      
      <v-card-actions class="pa-4">
        <v-btn
          text
          color="grey darken-1"
          @click="fechaModal"
        >
          Fechar
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          @click="$emit('atualizar')"
          :loading="carregandoHistoricoComparativo"
        >
          <v-icon left>mdi-refresh</v-icon>
          Atualizar Gráfico
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  mostrarGraficoComparativo: {
    type: Boolean,
    required: true
  },
  carregandoHistoricoComparativo: {
    type: Boolean,
    default: false
  },
  dadosHistoricoComparativo: {
    type: Array,
    default: () => []
  },
  grupoSelecionado: {
    type: Object,
    default: null
  },
  filtroGrafico: {
    type: Object,
    required: true
  },
  tiposProdutoFiltro: {
    type: Array,
    required: true
  },
  periodosFiltro: {
    type: Array,
    required: true
  },
  produtosParaFiltro: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['update:mostrar-grafico', 'fechar', 'filtro-changed', 'atualizar'])

const mostrarGrafico = ref(props.mostrarGraficoComparativo)
const chart = ref(null)
const chartContainer = ref(null)

// Sincronizar o v-model com a prop
watch(() => props.mostrarGraficoComparativo, (newVal) => {
  mostrarGrafico.value = newVal
})

watch(mostrarGrafico, (newVal) => {
  emit('update:mostrar-grafico', newVal)
})

const fechaModal = () => {
  emit('fechar')
}

// Expor refs para uso externo (renderização do gráfico)
defineExpose({
  chart,
  chartContainer
})
</script>

<style scoped>
/* Estilos específicos se necessário */
</style>
```