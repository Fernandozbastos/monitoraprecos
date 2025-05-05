<!-- frontend/src/components/product-detail/ClientPriceCard.vue -->
<template>
    <v-card v-if="produto.tipo_produto === 'cliente'" elevation="2" class="mb-4 detail-card">
      <v-card-title class="primary--text">
        <v-icon left color="primary">mdi-currency-usd</v-icon>
        Preço do Cliente
      </v-card-title>
      
      <v-card-text>
        <v-form ref="form" v-model="internalFormValid" class="py-3" @submit.prevent="handleSubmit">
          <v-text-field
            :model-value="precoCliente"
            @update:model-value="updatePreco"
            label="Preço do Cliente"
            prefix="R$"
            type="number"
            step="0.01"
            :rules="precoRules"
            filled
            rounded
            hide-details="auto"
            :loading="atualizandoPreco"
            :disabled="atualizandoPreco"
          ></v-text-field>
          <div class="caption text-grey mt-2">
            Este é o preço do seu produto. Atualize-o sempre que houver mudanças no valor.
          </div>
        </v-form>
      </v-card-text>
      
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          :disabled="!formValid"
          :loading="atualizandoPreco"
          @click="handleSubmit"
          elevation="2"
          class="px-6"
        >
          <v-icon left>mdi-content-save</v-icon>
          Atualizar Preço
        </v-btn>
      </v-card-actions>
    </v-card>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue'
  
  const props = defineProps({
    produto: {
      type: Object,
      required: true
    },
    precoCliente: {
      type: [Number, String],
      required: true
    },
    formValid: {
      type: Boolean,
      default: false
    },
    atualizandoPreco: {
      type: Boolean,
      default: false
    },
    precoRules: {
      type: Array,
      required: true
    }
  })
  
  const emit = defineEmits(['update:precoCliente', 'submit', 'update:formValid'])
  
  const form = ref(null)
  const internalFormValid = ref(props.formValid)
  
  // Sincronizar formValid interno com prop
  watch(() => props.formValid, (newVal) => {
    internalFormValid.value = newVal
  })
  
  // Emitir mudanças no form valid
  watch(internalFormValid, (newVal) => {
    emit('update:formValid', newVal)
  })
  
  const updatePreco = (value) => {
    emit('update:precoCliente', value)
  }
  
  const handleSubmit = async () => {
    const valid = await form.value?.validate()
    if (valid.valid) {
      emit('submit')
    }
  }
  </script>
  
  <style scoped>
  .detail-card {
    border-radius: 8px;
    overflow: hidden;
    transition: all 0.3s ease;
  }
  
  .detail-card:hover {
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
  }
  </style>