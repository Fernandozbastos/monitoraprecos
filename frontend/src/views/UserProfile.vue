<template>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h4 mb-4">Meu Perfil</h1>
        </v-col>
      </v-row>
      
      <v-row>
        <v-col cols="12" md="6">
          <v-card elevation="2" class="mb-4">
            <v-card-title>Informações do Usuário</v-card-title>
            <v-card-text>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-subtitle>Nome de Usuário</v-list-item-subtitle>
                  <v-list-item-title class="text-h6">{{ user.username }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-divider></v-divider>
              
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-subtitle>Email</v-list-item-subtitle>
                  <v-list-item-title>{{ user.email }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-divider></v-divider>
              
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-subtitle>Tipo de Usuário</v-list-item-subtitle>
                  <v-list-item-title>
                    {{ user.tipo === 'admin' ? 'Administrador' : 'Usuário' }}
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-divider></v-divider>
              
              <v-list-item v-if="user.cliente_atual">
                <v-list-item-content>
                  <v-list-item-subtitle>Cliente Atual</v-list-item-subtitle>
                  <v-list-item-title>{{ user.cliente_atual }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="12" md="6">
          <v-card elevation="2">
            <v-card-title>Alterar Senha</v-card-title>
            <v-card-text>
              <v-form ref="form" v-model="valid">
                <v-text-field
                  v-model="currentPassword"
                  :rules="passwordRules"
                  label="Senha Atual"
                  type="password"
                  required
                ></v-text-field>
                
                <v-text-field
                  v-model="newPassword"
                  :rules="passwordRules"
                  label="Nova Senha"
                  type="password"
                  required
                ></v-text-field>
                
                <v-text-field
                  v-model="confirmPassword"
                  :rules="[...passwordRules, passwordMatch]"
                  label="Confirmar Nova Senha"
                  type="password"
                  required
                ></v-text-field>
              </v-form>
              <v-alert
                v-if="success"
                type="success"
                dismissible
              >
                {{ success }}
              </v-alert>
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
                :disabled="!valid || loading"
                @click="alterarSenha"
              >
                Alterar Senha
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      
      <v-row class="mt-4">
        <v-col cols="12">
          <v-btn color="error" @click="handleLogout">
            <v-icon left>mdi-logout</v-icon>
            Sair
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { useStore } from 'vuex'
  import authService from '@/services/auth.service'
  
  const store = useStore()
  const form = ref(null)
  const valid = ref(false)
  const loading = ref(false)
  const currentPassword = ref('')
  const newPassword = ref('')
  const confirmPassword = ref('')
  const success = ref(null)
  const error = ref(null)
  
  const passwordRules = [
    v => !!v || 'Este campo é obrigatório',
    v => v.length >= 6 || 'A senha deve ter pelo menos 6 caracteres'
  ]
  
  const user = computed(() => store.getters['auth/user'])
  
  const passwordMatch = (value) => {
    return newPassword.value === value || 'As senhas não coincidem'
  }
  
  const alterarSenha = async () => {
    const isValid = await form.value?.validate()
    
    if (isValid?.valid) {
      loading.value = true
      error.value = null
      success.value = null
      
      try {
        await authService.changePassword({
          current_password: currentPassword.value,
          new_password: newPassword.value
        })
        
        success.value = 'Senha alterada com sucesso'
        currentPassword.value = ''
        newPassword.value = ''
        confirmPassword.value = ''
        form.value.reset()
      } catch (err) {
        error.value = err.response?.data?.detail || 'Erro ao alterar senha'
      } finally {
        loading.value = false
      }
    }
  }
  
  const handleLogout = () => {
    store.dispatch('auth/logout')
  }
  </script>