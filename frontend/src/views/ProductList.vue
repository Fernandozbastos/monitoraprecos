<template>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h4 mb-4">Produtos</h1>
        </v-col>
      </v-row>
      
      <v-row>
        <v-col cols="12">
          <v-card elevation="2">
            <v-card-title>
              <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Pesquisar"
                single-line
                hide-details
              ></v-text-field>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                :loading="loading"
                @click="carregarProdutos"
              >
                <v-icon left>mdi-refresh</v-icon>
                Atualizar
              </v-btn>
              <v-btn
                color="success"
                class="ml-2"
                @click="$router.push('/products/add')"
              >
                <v-icon left>mdi-plus</v-icon>
                Adicionar Produto
              </v-btn>
            </v-card-title>
            <v-card-text>
              <v-data-table
                :headers="headers"
                :items="produtos"
                :loading="loading"
                :search="search"
                :items-per-page="10"
                sort-by="nome"
                class="elevation-0"
              >
                <template v-slot:item.ultima_verificacao="{ item }">
                  {{ item.ultima_verificacao ? formatDate(item.ultima_verificacao) : 'Nunca' }}
                </template>
                <template v-slot:item.verificacao_manual="{ item }">
                  <v-icon v-if="item.verificacao_manual" color="warning">mdi-hand</v-icon>
                  <v-icon v-else color="success">mdi-robot</v-icon>
                </template>
                <template v-slot:item.actions="{ item }">
                  <v-btn
                    small
                    icon
                    color="primary"
                    @click="verDetalhes(item.id)"
                  >
                    <v-icon>mdi-eye</v-icon>
                  </v-btn>
                  <v-btn
                    small
                    icon
                    color="success"
                    @click="verificarPreco(item.id)"
                    :loading="verificandoItem === item.id"
                  >
                    <v-icon>mdi-refresh</v-icon>
                  </v-btn>
                  <v-btn
                    small
                    icon
                    color="warning"
                    @click="$router.push(`/products/${item.id}/edit`)"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import api from '@/services/api'
  
  const router = useRouter()
  const loading = ref(false)
  const produtos = ref([])
  const search = ref('')
  const verificandoItem = ref(null)
  
  const headers = [
    { title: 'Nome', key: 'nome' },
    { title: 'Concorrente', key: 'concorrente' },
    { title: 'Plataforma', key: 'plataforma_nome' },
    { title: 'Última Verificação', key: 'ultima_verificacao' },
    { title: 'Verificação Manual', key: 'verificacao_manual', align: 'center' },
    { title: 'Ações', key: 'actions', sortable: false, align: 'center' }
  ]
  
  onMounted(() => {
    carregarProdutos()
  })
  
  const carregarProdutos = async () => {
    loading.value = true
    try {
      const response = await api.get('/produtos/')
      produtos.value = response.data.results
    } catch (error) {
      console.error('Erro ao carregar produtos:', error)
    } finally {
      loading.value = false
    }
  }
  
  const formatDate = (dateString) => {
    const options = { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }
    return new Date(dateString).toLocaleString('pt-BR', options)
  }
  
  const verDetalhes = (id) => {
    router.push(`/products/${id}`)
  }
  
  const verificarPreco = async (id) => {
    verificandoItem.value = id
    try {
      await api.post(`/produtos/${id}/verificar/`)
      // Atualiza a lista após verificação
      carregarProdutos()
    } catch (error) {
      console.error('Erro ao verificar preço:', error)
    } finally {
      verificandoItem.value = null
    }
  }
  </script>