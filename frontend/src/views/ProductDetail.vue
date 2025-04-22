<template>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-btn text @click="$router.go(-1)" class="mb-4">
            <v-icon left>mdi-arrow-left</v-icon>
            Voltar
          </v-btn>
          <h1 class="text-h4 mb-4">{{ produto.nome || 'Detalhes do Produto' }}</h1>
        </v-col>
      </v-row>
      
      <v-row v-if="loading">
        <v-col cols="12" class="text-center">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-col>
      </v-row>
      
      <template v-else>
        <v-row>
          <v-col cols="12" md="6">
            <v-card elevation="2" class="mb-4">
              <v-card-title>Informações do Produto</v-card-title>
              <v-card-text>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle>Nome</v-list-item-subtitle>
                    <v-list-item-title class="text-h6">{{ produto.nome || 'N/A' }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle>Concorrente</v-list-item-subtitle>
                    <v-list-item-title>{{ produto.concorrente || 'N/A' }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle>URL</v-list-item-subtitle>
                    <v-list-item-title>
                      <a :href="produto.url" target="_blank" rel="noopener noreferrer" v-if="produto.url">
                        {{ produto.url }}
                      </a>
                      <span v-else>N/A</span>
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle>Plataforma</v-list-item-subtitle>
                    <v-list-item-title>{{ produto.plataforma?.nome || 'N/A' }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle>Última Verificação</v-list-item-subtitle>
                    <v-list-item-title>{{ formatDate(produto.ultima_verificacao) }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-card-text>
              <v-card-actions>
                <v-btn 
                  color="primary" 
                  @click="verificarPreco" 
                  :loading="verificando"
                >
                  <v-icon left>mdi-refresh</v-icon>
                  Verificar Preço Agora
                </v-btn>
                <v-btn 
                  v-if="produto.url"
                  text
                  color="secondary"
                  :href="produto.url" 
                  target="_blank"
                >
                  <v-icon left>mdi-open-in-new</v-icon>
                  Abrir Site
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="6">
            <!-- Cards de preço removidos pois podem estar causando o erro -->
          </v-col>
        </v-row>
      </template>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import axios from 'axios'
  
  const route = useRoute()
  const router = useRouter()
  const loading = ref(true)
  const verificando = ref(false)
  const produto = ref({})
  const historico = ref([])
  
  // Formatação de data
  const formatDate = (dateString) => {
    if (!dateString) return 'Nunca';
    const options = { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' };
    try {
      return new Date(dateString).toLocaleString('pt-BR', options);
    } catch (e) {
      console.error('Erro ao formatar data:', e);
      return dateString;
    }
  }
  
  // Carregar informações do produto
  const carregarProduto = async () => {
    loading.value = true;
    try {
      // URL base da API
      const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
      
      // Token de autenticação do localStorage
      const token = localStorage.getItem('accessToken');
      if (!token) {
        console.error('Token não encontrado, redirecionando para login');
        router.push('/login');
        return;
      }
      
      const config = {
        headers: { Authorization: `Bearer ${token}` }
      };
      
      const produtoId = route.params.id;
      console.log('Carregando produto com ID:', produtoId);
      
      // Buscar o produto
      const response = await axios.get(`${baseURL}/produtos/${produtoId}/`, config);
      produto.value = response.data;
      console.log('Produto carregado:', produto.value);
      
    } catch (error) {
      console.error('Erro ao carregar produto:', error);
      produto.value = {};
    } finally {
      loading.value = false;
    }
  }
  
  // Verificar preço manualmente
  const verificarPreco = async () => {
    if (!produto.value.id) {
      console.error('ID do produto não disponível');
      return;
    }
    
    verificando.value = true;
    try {
      // URL base da API
      const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
      
      // Token de autenticação do localStorage
      const token = localStorage.getItem('accessToken');
      
      const config = {
        headers: { Authorization: `Bearer ${token}` }
      };
      
      // Chamada para verificar o preço (ajuste conforme a API)
      await axios.post(`${baseURL}/produtos/${produto.value.id}/verificar/`, {}, config);
      
      // Recarregar o produto com os dados atualizados
      await carregarProduto();
      
    } catch (error) {
      console.error('Erro ao verificar preço:', error);
    } finally {
      verificando.value = false;
    }
  }
  
  // Carregar ao montar o componente
  onMounted(() => {
    carregarProduto();
  });
  
  // Observar mudanças no ID do produto na rota
  watch(() => route.params.id, (newId, oldId) => {
    if (newId !== oldId) {
      carregarProduto();
    }
  });
  </script>