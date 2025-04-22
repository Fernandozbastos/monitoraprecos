<template>
    <v-container class="fill-height" fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card class="elevation-12">
            <v-toolbar color="primary" dark flat>
              <v-toolbar-title>MonitoraPreços - Login</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form ref="form" @submit.prevent="handleLogin">
                <v-text-field
                  v-model="username"
                  :rules="usernameRules"
                  label="Usuário"
                  name="username"
                  prepend-icon="mdi-account"
                  type="text"
                  required
                ></v-text-field>
  
                <v-text-field
                  v-model="password"
                  :rules="passwordRules"
                  label="Senha"
                  name="password"
                  prepend-icon="mdi-lock"
                  type="password"
                  @keyup.enter="handleLogin"
                  required
                ></v-text-field>
              </v-form>
              <v-alert
                v-if="error"
                type="error"
                dismissible
              >
                {{ error }}
              </v-alert>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn 
                color="primary" 
                :loading="loading" 
                :disabled="loading" 
                @click="handleLogin"
              >
                Entrar
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { useStore } from 'vuex'
  import { useRouter } from 'vue-router'
  
  const store = useStore()
  const router = useRouter()
  
  // Estado
  const username = ref('')
  const password = ref('')
  const form = ref(null)
  
  // Regras de validação
  const usernameRules = [
    v => !!v || 'Usuário é obrigatório',
  ]
  const passwordRules = [
    v => !!v || 'Senha é obrigatória',
  ]
  
  // Computed properties
  const loading = computed(() => store.getters['auth/loading'])
  const error = computed(() => store.getters['auth/error'])
  
  // Métodos
  const handleLogin = async () => {
    const isValid = await form.value?.validate()
    
    if (isValid?.valid) {
      try {
        await store.dispatch('auth/login', {
          username: username.value,
          password: password.value
        })
        // O redirecionamento é feito na ação login
      } catch (error) {
        // Erro já é tratado na action
      }
    }
  }
  </script>