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
                    <v-list-item-subtitle>Tipo</v-list-item-subtitle>
                    <v-list-item-title>
                      {{ produto.tipo_produto === 'cliente' ? 'Produto do Cliente' : 'Produto de Concorrente' }}
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item v-if="produto.tipo_produto === 'concorrente'">
                  <v-list-item-content>
                    <v-list-item-subtitle>Concorrente</v-list-item-subtitle>
                    <v-list-item-title>{{ produto.concorrente || 'N/A' }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-divider v-if="produto.tipo_produto === 'concorrente'"></v-divider>
                
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
            <!-- Preço do Cliente (apenas para produtos do cliente) -->
            <v-card v-if="produto.tipo_produto === 'cliente'" elevation="2" class="mb-4">
              <v-card-title>Preço do Cliente</v-card-title>
              <v-card-text>
                <v-form ref="form" v-model="formValid">
                  <v-text-field
                    v-model="precoCliente"
                    label="Preço do Cliente"
                    prefix="R$"
                    type="number"
                    step="0.01"
                    :rules="precoRules"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="primary"
                  :disabled="!formValid"
                  :loading="atualizandoPreco"
                  @click="atualizarPrecoCliente"
                >
                  Atualizar Preço
                </v-btn>
              </v-card-actions>
            </v-card>
            
            <!-- Comparação de Preços (apenas para produtos do cliente) -->
            <v-card v-if="produto.tipo_produto === 'cliente'" elevation="2" class="mb-4">
              <v-card-title>
                Comparação de Preços
              </v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-subtitle>Preço do Cliente</v-list-item-subtitle>
                      <v-list-item-title class="text-h6">
                        {{ formatarPreco(produto.preco_cliente) }}
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-subtitle>Menor Preço Concorrente</v-list-item-subtitle>
                      <v-list-item-title class="text-h6">
                        {{ formatarPreco(produto.menor_preco_concorrente) }}
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  
                  <v-list-item v-if="produto.diferenca_percentual !== null">
                    <v-list-item-content>
                      <v-list-item-subtitle>Diferença Percentual</v-list-item-subtitle>
                      <v-list-item-title>
                        <v-chip
                          :color="produto.diferenca_percentual <= 0 ? 'success' : 'error'"
                          class="font-weight-bold"
                        >
                          {{ formatarPercentual(produto.diferenca_percentual) }}
                        </v-chip>
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
            
            <!-- Alerta se não houver concorrentes -->
            <v-alert
              v-if="produto.tipo_produto === 'cliente' && produto.menor_preco_concorrente === null"
              type="warning"
              class="mb-4"
            >
              Não há preços de concorrentes registrados para esse produto. Cadastre produtos concorrentes com o mesmo nome para habilitar a comparação.
            </v-alert>
          </v-col>
        </v-row>
      </template>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted, watch, computed } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import api from '@/services/api'
  
  const route = useRoute()
  const router = useRouter()
  const loading = ref(true)
  const verificando = ref(false)
  const atualizandoPreco = ref(false)
  const produto = ref({})
  const precoCliente = ref(0)
  const formValid = ref(false)
  const form = ref(null)
  
  // Regras de validação
  const precoRules = [
    v => !!v || 'O preço é obrigatório',
    v => v > 0 || 'O preço deve ser maior que zero'
  ]
  
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
  
  // Formatação de preço
  const formatarPreco = (valor) => {
    if (valor === null || valor === undefined) return 'N/A'
    return `R$ ${Number(valor).toFixed(2).replace('.', ',')}`
  }
  
  // Formatação de percentual
  const formatarPercentual = (valor) => {
    if (valor === null || valor === undefined) return 'N/A'
    const sinal = valor > 0 ? '+' : ''
    return `${sinal}${valor.toFixed(1).replace('.', ',')}%`
  }
  
  // Carregar informações do produto
  const carregarProduto = async () => {
    loading.value = true;
    try {
      const produtoId = route.params.id;
      console.log('Carregando produto com ID:', produtoId);
      
      // Buscar o produto
      const response = await api.get(`/produtos/${produtoId}/`);
      produto.value = response.data;
      console.log('Produto carregado:', produto.value);
      
      // Atualiza o campo de preço para produtos do cliente
      if (produto.value.tipo_produto === 'cliente' && produto.value.preco_cliente !== null) {
        precoCliente.value = produto.value.preco_cliente;
      }
      
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
      // Chamada para verificar o preço
      await api.post(`/produtos/${produto.value.id}/verificar/`);
      
      // Recarregar o produto com os dados atualizados
      await carregarProduto();
      
    } catch (error) {
      console.error('Erro ao verificar preço:', error);
    } finally {
      verificando.value = false;
    }
  }
  
  // Atualizar preço do cliente
  const atualizarPrecoCliente = async () => {
    if (!produto.value.id || produto.value.tipo_produto !== 'cliente') {
      console.error('Operação não permitida');
      return;
    }
    
    atualizandoPreco.value = true;
    try {
      // Chamar o endpoint para atualizar o preço do cliente
      await api.post(`/produtos/${produto.value.id}/atualizar_preco_cliente/`, {
        preco_cliente: precoCliente.value
      });
      
      // Recarregar o produto com os dados atualizados
      await carregarProduto();
      
    } catch (error) {
      console.error('Erro ao atualizar preço do cliente:', error);
    } finally {
      atualizandoPreco.value = false;
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
  
  <style scoped>
  .v-chip {
    font-weight: bold;
  }
  </style>