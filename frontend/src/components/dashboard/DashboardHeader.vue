<template>
    <v-row>
      <v-col cols="12">
        <v-card elevation="2" class="mb-6 gradient-header">
          <v-card-text>
            <div class="d-flex flex-wrap align-center">
              <div>
                <h1 class="text-h4 font-weight-bold white--text mb-1">{{ title }}</h1>
                <p class="text-subtitle-1 white--text mb-0">{{ subtitle }}</p>
              </div>
              <v-spacer></v-spacer>
              <slot name="actions">
                <!-- Slot para ações personalizadas -->
                <v-btn
                  color="white"
                  class="primary--text text-none px-4 elevation-1"
                  @click="$emit('add-product')"
                >
                  <v-icon left>mdi-plus</v-icon>
                  {{ buttonText }}
                </v-btn>
              </slot>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </template>
  
  <script setup>
  defineProps({
    title: {
      type: String,
      default: 'Dashboard'
    },
    subtitle: {
      type: String,
      default: 'Monitore seus produtos e concorrentes'
    },
    buttonText: {
      type: String,
      default: 'Adicionar Produto'
    }
  })
  
  defineEmits(['add-product'])
  </script>
  
  <style scoped>
  .gradient-header {
    background: linear-gradient(135deg, var(--v-primary-base) 0%, var(--v-primary-darken1) 100%);
    border-radius: 8px;
  }
  </style>