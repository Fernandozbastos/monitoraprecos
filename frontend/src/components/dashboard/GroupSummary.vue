<template>
    <div class="d-none d-md-flex align-center">
      <!-- Preço do cliente -->
      <div class="text-center mx-3 resumo-grupo">
        <div class="caption grey--text">Preço Cliente</div>
        <div class="subtitle-1 font-weight-medium primary--text">
          {{ 
            grupo.produtoClienteBase.preco_cliente ? 
            formatarPreco(grupo.produtoClienteBase.preco_cliente) : 
            'N/A' 
          }}
        </div>
      </div>
      
      <!-- Menor preço concorrente -->
      <div class="text-center mx-3 resumo-grupo">
        <div class="caption grey--text">Menor Preço</div>
        <div class="subtitle-1 font-weight-medium">
          {{ 
            grupo.menorPrecoConcorrente ? 
            formatarPreco(grupo.menorPrecoConcorrente) : 
            'N/A' 
          }}
        </div>
      </div>
      
      <!-- Diferença percentual -->
      <div class="text-center mx-3" v-if="grupo.diferencaPercentual !== null">
        <div class="caption grey--text">Variação</div>
        <v-chip
          small
          :color="getCorDiferenca(grupo.diferencaPercentual)"
          dark
        >
          {{ formatarPercentual(grupo.diferencaPercentual) }}
        </v-chip>
      </div>
      
      <!-- Concorrente com menor preço -->
      <div class="text-center mx-3" v-if="grupo.concorrenteMenorPreco">
        <div class="caption grey--text">Concorrente</div>
        <div class="subtitle-2 font-weight-regular text-truncate" style="max-width: 150px">
          {{ grupo.concorrenteMenorPreco }}
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { formatarPreco, formatarPercentual, getCorDiferenca } from '@/utils/formatters'
  
  defineProps({
    grupo: {
      type: Object,
      required: true
    }
  })
  </script>
  
  <style scoped>
  .resumo-grupo {
    position: relative;
  }
  
  .resumo-grupo::after {
    content: "";
    position: absolute;
    right: -18px;
    top: 50%;
    height: 30px;
    border-right: 1px solid rgba(0, 0, 0, 0.12);
    transform: translateY(-50%);
  }
  
  .resumo-grupo:last-child::after {
    display: none;
  }
  </style>