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
                  v => /^https?:\/\/.+/.test(v) || 'URL deve começar com http:// ou https://',
                  v => v.length <= 1000 || 'URL não pode exceder 1000 caracteres'
                ]"
                label="URL do Produto"
                hint="Insira a URL completa da página do produto"
                persistent-hint
                required
              >
                <template v-slot:append>
                  <v-btn 
                    icon 
                    small 
                    v-if="produto.url" 
                    @click="abrirUrlPrevia"
                  >
                    <v-icon>mdi-open-in-new</v-icon>
                  </v-btn>
                </template>
              </v-text-field>
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
            
            <!-- Seletor de grupo oculto, será preenchido automaticamente -->
            <!-- 
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
            -->
            
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

const abrirUrlPrevia = () => {
  if (produto.value.url) {
    window.open(produto.value.url, '_blank');
  }
}

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
  verificacao_manual: false,
  tipo_produto: 'concorrente'
})

// Notificações
const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

// Detecta se é modo de edição ou criação
const isEditMode = computed(() => !!route.params.id)

// Função para diagnosticar os dados antes do envio
const diagnosticarDados = (userInfo, produtoParaEnviar) => {
  console.log('====== DIAGNÓSTICO DOS DADOS ======');
  console.log('Usuário:', userInfo.data);
  console.log('Cliente atual:', userInfo.data.cliente_atual);
  console.log('Produto a enviar:', produtoParaEnviar);
  console.log('Tipo do cliente:', typeof produtoParaEnviar.cliente);
  console.log('Tipo do grupo:', typeof produtoParaEnviar.grupo);
  console.log('===================================');
}

// Função para obter e aplicar o grupo do usuário ao produto
const aplicarGrupoUsuario = async () => {
  try {
    // Obter informações do usuário
    const userInfo = await api.get('/user/info/')
    
    // Obter grupos vinculados ao cliente atual do usuário
    if (userInfo.data.cliente_atual) {
      // Carregar grupos associados ao cliente atual
      const gruposResponse = await api.get(`/grupos/?cliente=${userInfo.data.cliente_atual}`);
      if (gruposResponse.data.results && gruposResponse.data.results.length > 0) {
        // Aplicar o primeiro grupo disponível
        produto.value.grupo = gruposResponse.data.results[0].id;
        console.log('Grupo aplicado automaticamente:', produto.value.grupo);
      } else {
        console.warn('Nenhum grupo disponível para o cliente atual');
      }
    }
  } catch (error) {
    console.error('Erro ao obter grupo do usuário:', error);
  }
}

// Carregar dados iniciais
onMounted(async () => {
  await Promise.all([carregarPlataformas(), carregarGrupos()])
  
  if (isEditMode.value) {
    await carregarProduto(route.params.id)
  } else {
    // Aplicar grupo automaticamente para novos produtos
    await aplicarGrupoUsuario()
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
    // Obter o cliente atual do usuário
    const userInfo = await api.get('/user/info/')
    if (userInfo.data.cliente_atual) {
      // Carregar apenas grupos associados ao cliente atual
      const response = await api.get(`/grupos/?cliente=${userInfo.data.cliente_atual}`)
      grupos.value = response.data.results || []
    } else {
      grupos.value = []
    }
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
      // Obtém o cliente atual do usuário
      const userInfo = await api.get('/user/info/')
      
      // Verifica se o cliente_atual está definido
      if (!userInfo.data.cliente_atual) {
        mostrarSnackbar('Você precisa selecionar um cliente atual antes de adicionar um produto', 'error')
        loading.value = false
        return
      }
      
      // Verifica se cliente_atual é um objeto ou um ID
      const clienteId = typeof userInfo.data.cliente_atual === 'object' 
        ? userInfo.data.cliente_atual.id 
        : userInfo.data.cliente_atual
        
      console.log('Cliente ID obtido:', clienteId)
      
      // Obter o ID do grupo se for um objeto
      let grupoId = null
      if (produto.value.grupo) {
        grupoId = typeof produto.value.grupo === 'object' 
          ? produto.value.grupo.id 
          : produto.value.grupo
      } else if (grupos.value && grupos.value.length > 0) {
        // Se não tiver grupo selecionado, use o primeiro disponível
        grupoId = grupos.value[0].id
      }
      
      // Obter o ID da plataforma se for um objeto
      let plataformaId = null
      if (produto.value.plataforma) {
        plataformaId = typeof produto.value.plataforma === 'object' 
          ? produto.value.plataforma.id 
          : produto.value.plataforma
      }
      
      // Cria uma cópia do produto com apenas os campos necessários e garantindo que IDs sejam usados
      const produtoParaEnviar = {
        nome: produto.value.nome,
        concorrente: produto.value.concorrente,
        url: produto.value.url,
        verificacao_manual: produto.value.verificacao_manual || false,
        tipo_produto: produto.value.tipo_produto || 'concorrente',
        cliente: clienteId,  // Usar o ID do cliente
        grupo: grupoId       // Usar o ID do grupo
      }
      
      // Adicionar plataforma apenas se estiver definida
      if (plataformaId) {
        produtoParaEnviar.plataforma = plataformaId
      }

      // Diagnóstico mais detalhado
      console.log('====== DIAGNÓSTICO DETALHADO DOS DADOS ======')
      console.log('Produto original:', produto.value)
      console.log('Cliente atual (userInfo):', userInfo.data.cliente_atual)
      console.log('Cliente ID processado:', clienteId)
      console.log('Grupo ID processado:', grupoId)
      console.log('Produto preparado para envio:', produtoParaEnviar)
      console.log('=============================================')
      
      // Verificações finais para campos obrigatórios
      if (!produtoParaEnviar.cliente) {
        mostrarSnackbar('Erro: Cliente não selecionado. Por favor, selecione um cliente no menu superior.', 'error')
        loading.value = false
        return
      }

      if (!produtoParaEnviar.grupo) {
        mostrarSnackbar('Erro: Nenhum grupo disponível para este cliente', 'error')
        loading.value = false
        return
      }
      
      let response;
      if (isEditMode.value) {
        response = await api.put(`/produtos/${produto.value.id}/`, produtoParaEnviar)
        console.log('Resposta de atualização:', response.data)
        mostrarSnackbar('Produto atualizado com sucesso')
      } else {
        response = await api.post('/produtos/', produtoParaEnviar)
        console.log('Resposta de criação:', response.data)
        mostrarSnackbar('Produto adicionado com sucesso')
      }
      router.push('/products')
    } catch (error) {
      console.error('Erro ao salvar produto:', error)
      console.error('Detalhes do erro:', error.response?.data)
      mostrarSnackbar(
        'Erro ao salvar produto: ' + (error.response?.data?.detail || error.message), 
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