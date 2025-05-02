<template>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h4 mb-4">{{ isEditMode ? 'Editar Produto' : 'Adicionar Produto' }}</h1>
        </v-col>
      </v-row>
      
      <v-form ref="form" v-model="valid" @submit.prevent="onSubmit">
        <v-card elevation="2">
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="produto.nome"
                  :rules="[v => !!v || 'Nome é obrigatório']"
                  label="Nome do Produto"
                  required
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="produto.concorrente"
                  :rules="[v => !!v || 'Concorrente é obrigatório']"
                  label="Concorrente"
                  required
                ></v-text-field>
              </v-col>
              
              <v-col cols="12">
                <v-text-field
                  v-model="produto.url"
                  :rules="[
                    v => !!v || 'URL é obrigatória',
                    v => /^https?:\/\/.+/.test(v) || 'URL deve começar com http:// ou https://'
                  ]"
                  label="URL do Produto"
                  required
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-select
                  v-model="produto.plataforma"
                  :items="plataformas"
                  item-title="nome"
                  item-value="id"
                  label="Plataforma"
                  return-object
                  :loading="loadingPlataformas"
                ></v-select>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-select
                  v-model="produto.grupo"
                  :items="grupos"
                  item-title="nome"
                  item-value="id"
                  label="Grupo"
                  required
                  :rules="[v => !!v || 'Grupo é obrigatório']"
                  :loading="loadingGrupos"
                ></v-select>
              </v-col>
              
              <v-col cols="12">
                <v-switch
                  v-model="produto.verificacao_manual"
                  label="Verificação Manual"
                  hint="Se ativado, o produto não será verificado automaticamente"
                  persistent-hint
                ></v-switch>
              </v-col>
            </v-row>
          </v-card-text>
          
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="$router.go(-1)">Cancelar</v-btn>
            <v-btn
              color="primary"
              type="submit"
              :loading="loading"
              :disabled="!valid || loading"
            >
              {{ isEditMode ? 'Atualizar' : 'Salvar' }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
      
      <v-snackbar
        v-model="snackbar.show"
        :color="snackbar.color"
        timeout="3000"
      >
        {{ snackbar.text }}
      </v-snackbar>
    </v-container>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import api from '@/services/api'
  
  const route = useRoute()
  const router = useRouter()
  
  // Estado do formulário
  const form = ref(null)
  const valid = ref(false)
  const loading = ref(false)
  const loadingPlataformas = ref(false)
  const loadingGrupos = ref(false)
  
  // Lista de plataformas e grupos
  const plataformas = ref([])
  const grupos = ref([])
  
  // Dados do produto
  const produto = ref({
    nome: '',
    concorrente: '',
    url: '',
    plataforma: null,
    grupo: null,
    verificacao_manual: false
  })
  
  // Notificações
  const snackbar = ref({
    show: false,
    text: '',
    color: 'success'
  })
  
  // Detecta se é modo de edição ou criação
  const isEditMode = computed(() => !!route.params.id)
  
  // Carregar dados iniciais
  onMounted(async () => {
    await Promise.all([carregarPlataformas(), carregarGrupos()])
    
    if (isEditMode.value) {
      await carregarProduto(route.params.id)
    }
  })
  
  // Carregar plataformas disponíveis
  const carregarPlataformas = async () => {
    loadingPlataformas.value = true
    try {
      const response = await api.get('/plataformas/')
      plataformas.value = response.data.results || []
    } catch (error) {
      console.error('Erro ao carregar plataformas:', error)
      mostrarSnackbar('Erro ao carregar plataformas', 'error')
    } finally {
      loadingPlataformas.value = false
    }
  }
  
  // Carregar grupos disponíveis
  const carregarGrupos = async () => {
    loadingGrupos.value = true
    try {
      const response = await api.get('/grupos/')
      grupos.value = response.data.results || []
    } catch (error) {
      console.error('Erro ao carregar grupos:', error)
      mostrarSnackbar('Erro ao carregar grupos', 'error')
    } finally {
      loadingGrupos.value = false
    }
  }
  
  // Carregar dados do produto para edição
  const carregarProduto = async (id) => {
    loading.value = true
    try {
      const response = await api.get(`/produtos/${id}/`)
      produto.value = response.data
    } catch (error) {
      console.error('Erro ao carregar produto:', error)
      mostrarSnackbar('Erro ao carregar produto', 'error')
      router.push('/products')
    } finally {
      loading.value = false
    }
  }
  
  // Salvar ou atualizar produto
  const onSubmit = async () => {
    const isValid = await form.value?.validate()
    
    if (isValid?.valid) {
      loading.value = true
      try {
        if (isEditMode.value) {
          await api.put(`/produtos/${produto.value.id}/`, produto.value)
          mostrarSnackbar('Produto atualizado com sucesso')
        } else {
          await api.post('/produtos/', produto.value)
          mostrarSnackbar('Produto adicionado com sucesso')
        }
        router.push('/products')
      } catch (error) {
        console.error('Erro ao salvar produto:', error)
        mostrarSnackbar(
          error.response?.data?.detail || 'Erro ao salvar produto', 
          'error'
        )
      } finally {
        loading.value = false
      }
    }
  }
  
  // Mostrar mensagem de feedback
  const mostrarSnackbar = (text, color = 'success') => {
    snackbar.value = {
      show: true,
      text,
      color
    }
  }
  </script>