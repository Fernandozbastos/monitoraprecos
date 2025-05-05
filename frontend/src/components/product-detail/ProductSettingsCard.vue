<!-- frontend/src/components/product-detail/ProductSettingsCard.vue -->
<template>
    <v-card 
      v-if="mostrarCard" 
      elevation="2" 
      class="mb-4"
      :class="{'warning-card': inconsistente}"
    >
      <v-card-title 
        :class="inconsistente ? 'warning--text' : 'primary--text'"
      >
        <v-icon 
          left 
          :color="inconsistente ? 'warning' : 'primary'"
        >
          {{ inconsistente ? 'mdi-alert-circle' : 'mdi-star' }}
        </v-icon>
        {{ inconsistente ? 'Atenção: Configuração Inconsistente' : 'Produto Cliente Base' }}
      </v-card-title>
      
      <v-card-text>
        <template v-if="inconsistente">
          <v-alert type="warning" class="mb-4" dense>
            Este produto está marcado como produto cliente base, mas é do tipo concorrente. 
            O ideal é que o produto cliente base seja do tipo "cliente" para funcionamento correto do sistema.
          </v-alert>
          
          <v-sheet class="pa-4 rounded text-center" color="grey lighten-4">
            <div class="text-subtitle-1 mb-2">Preço Mais Recente:</div>
            <div class="text-h4 font-weight-bold primary--text">
              {{ produto.preco_exibicao ? formatarPreco(produto.preco_exibicao) : formatarPreco(produto.menor_preco_concorrente) }}
            </div>
          </v-sheet>
          
          <div class="caption text-grey mt-3">
            Este é o preço mais recente registrado para este produto. Considere alterar o tipo para "cliente" 
            para melhor organização do sistema.
          </div>
          
          <div class="mt-6">
            <v-btn
              color="primary"
              @click="$emit('corrigir-tipo')"
              :loading="corrigindoTipo"
            >
              <v-icon left>mdi-check</v-icon>
              Corrigir Tipo para Cliente
            </v-btn>
          </div>
        </template>
        
        <template v-else>
          <v-list>
            <v-list-item>
              <v-list-item-avatar color="amber" class="rounded white--text">
                <v-icon>mdi-star</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title class="text-subtitle-2 text-gray">Produto Cliente Base</v-list-item-title>
                <div class="mt-2">
                  <v-switch
                    :model-value="produto.produto_cliente"
                    @update:model-value="handleToggle"
                    :disabled="atualizandoStatus || (produto.tipo_produto !== 'cliente' && produto.tipo_produto !== 'concorrente')"
                    color="primary"
                    hide-details
                    dense
                  ></v-switch>
                  <div class="caption mt-1 text-grey">
                    Este produto será usado como base para comparações de preço
                  </div>
                </div>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </template>
      </v-card-text>
    </v-card>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    produto: {
      type: Object,
      required: true
    },
    atualizandoStatus: {
      type: Boolean,
      default: false
    },
    corrigindoTipo: {
      type: Boolean,
      default: false
    },
    formatarPreco: {
      type: Function,
      required: true
    }
  })
  
  const emit = defineEmits(['update-status', 'corrigir-tipo'])
  
  const inconsistente = computed(() => {
    return props.produto.tipo_produto === 'concorrente' && props.produto.produto_cliente
  })
  
  const mostrarCard = computed(() => {
    // Mostra o card se o produto for do tipo cliente ou se for inconsistente
    return props.produto.tipo_produto === 'cliente' || inconsistente.value
  })
  
  const handleToggle = () => {
    emit('update-status')
  }
  </script>
  
  <style scoped>
  .warning-card {
    border-left: 4px solid var(--v-warning-base);
    border-radius: 8px;
    overflow: hidden;
  }
  </style>