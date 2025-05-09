<!-- frontend/src/views/ProductForm.vue -->
<template>
  <v-container fluid>
    <!-- Cabeçalho -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="3" class="mb-6 gradient-header">
          <v-card-text class="pa-6">
            <div class="d-flex align-center">
              <div>
                <h1 class="text-h4 white--text mb-1">{{ isEditMode ? 'Editar Produto' : 'Adicionar Produto' }}</h1>
                <p class="text-subtitle-1 white--text mb-0">
                  {{ isEditMode ? 'Atualize as informações do produto' : 'Cadastre um novo produto para monitoramento' }}
                </p>
              </div>
              <v-spacer></v-spacer>
              <v-btn
                icon
                color="white"
                @click="$router.go(-1)"
              >
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Formulário principal -->
    <v-form ref="form" v-model="valid" @submit.prevent="onSubmit">
      <v-card elevation="2" class="form-card">
        <v-tabs
          v-model="activeTab"
          background-color="primary"
          dark
          grow
        >
          <v-tab>
            <v-icon left>mdi-information-outline</v-icon>
            Informações Básicas
          </v-tab>
          <v-tab>
            <v-icon left>mdi-web</v-icon>
            URL e Plataforma
          </v-tab>
          <v-tab>
            <v-icon left>mdi-cog-outline</v-icon>
            Configurações
          </v-tab>
        </v-tabs>
        
        <v-tabs-items v-model="activeTab">
          <!-- Aba 1: Informações Básicas -->
          <v-tab-item>
            <v-card-text class="pa-6">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="produto.nome"
                    :rules="[v => !!v || 'Nome é obrigatório']"
                    label="Nome do Produto"
                    filled
                    hide-details="auto"
                    prepend-icon="mdi-tag"
                    required
                  ></v-text-field>
                  <div class="caption text-grey ml-12 mt-1">
                    Use o mesmo nome para produtos similares de diferentes concorrentes para facilitar comparações.
                  </div>
                </v-col>
                
                <v-col cols="12" md="6">
                  <v-select
                    v-model="produto.tipo_produto"
                    :items="tiposProduto"
                    item-text="texto"
                    item-value="valor"
                    label="Tipo de Produto"
                    filled
                    hide-details="auto"
                    prepend-icon="mdi-store"
                    required
                  ></v-select>
                  <div class="caption text-grey ml-12 mt-1">
                    Produtos do tipo "Cliente" são seus próprios produtos. Produtos "Concorrentes" são de outras empresas.
                  </div>
                </v-col>
                
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="produto.concorrente"
                    :rules="[v => !!v || 'Concorrente/Marca é obrigatório']"
                    label="Concorrente / Marca"
                    filled
                    hide-details="auto"
                    prepend-icon="mdi-account-group"
                    required
                  ></v-text-field>
                  <div class="caption text-grey ml-12 mt-1">
                    Nome da empresa concorrente ou sua própria marca para produtos do cliente.
                  </div>
                </v-col>
                
                <v-col cols="12" md="6" v-if="produto.tipo_produto === 'cliente'">
                  <v-text-field
                    v-model="produto.preco_cliente"
                    label="Preço do Produto (R$)"
                    filled
                    type="number"
                    step="0.01"
                    hide-details="auto"
                    prefix="R$"
                    prepend-icon="mdi-currency-usd"
                  ></v-text-field>
                  <div class="caption text-grey ml-12 mt-1">
                    Preço atual do seu produto. Você pode atualizar isso mais tarde.
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-tab-item>
          
          <!-- Aba 2: URL e Plataforma -->
          <v-tab-item>
            <v-card-text class="pa-6">
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="produto.url"
                    :rules="[
                      v => !!v || 'URL é obrigatória',
                      v => /^https?:\/\/.+/.test(v) || 'URL deve começar com http:// ou https://',
                      v => v.length <= 1000 || 'URL não pode exceder 1000 caracteres'
                    ]"
                    label="URL do Produto"
                    filled
                    hide-details="auto"
                    prepend-icon="mdi-link-variant"
                    required
                  >
                    <template v-slot:append>
                      <v-btn 
                        icon 
                        small 
                        v-if="produto.url" 
                        @click="abrirUrlPrevia"
                        color="primary"
                      >
                        <v-icon>mdi-open-in-new</v-icon>
                      </v-btn>
                    </template>
                  </v-text-field>
                  <div class="caption text-grey ml-12 mt-1">
                    URL completa da página do produto que deseja monitorar.
                  </div>
                </v-col>
                
                <v-col cols="12" md="6">
                  <v-select
                    v-model="produto.plataforma"
                    :items="plataformas"
                    item-text="nome"
                    item-value="id"
                    label="Plataforma"
                    filled
                    hide-details="auto"
                    prepend-icon="mdi-web"
                    :loading="loadingPlataformas"
                    return-object
                  ></v-select>
                  <div class="caption text-grey ml-12 mt-1">
                    Escolha a plataforma ou site onde o produto está hospedado.
                  </div>
                </v-col>
                
                <v-col cols="12" md="6">
                  <v-autocomplete
                    v-model="dominioSelecionado"
                    :items="dominiosDisponiveis"
                    item-text="nome"
                    label="Domínio Detectado"
                    filled
                    hide-details="auto"
                    prepend-icon="mdi-web"
                    readonly
                    disabled
                  ></v-autocomplete>
                  <div class="caption text-grey ml-12 mt-1">
                    Domínio detectado automaticamente a partir da URL.
                  </div>
                </v-col>
              </v-row>
              
              <!-- Alerta de previsualização -->
              <v-alert
                v-if="produto.url && produto.plataforma"
                color="info"
                outlined
                class="mt-4"
                icon="mdi-information"
              >
                <div class="d-flex align-center">
                  <div class="flex-grow-1">
                    <strong>Seletor de preço:</strong> {{ produto.plataforma ? produto.plataforma.seletor_css || 'Não definido' : 'Não definido' }}
                  </div>
                  <v-btn
                    color="info"
                    text
                    @click="testarSeletor"
                    :loading="testandoSeletor"
                  >
                    <v-icon left>mdi-test-tube</v-icon>
                    Testar Extração
                  </v-btn>
                </div>
              </v-alert>
              
              <!-- Resultado do teste de extração -->
              <v-expand-transition>
                <v-sheet
                  v-if="resultadoTeste"
                  class="pa-4 mt-3"
                  :color="resultadoTeste.sucesso ? 'success lighten-4' : 'error lighten-4'"
                  rounded
                >
                  <div class="d-flex align-center">
                    <v-icon 
                      :color="resultadoTeste.sucesso ? 'success' : 'error'"
                      class="mr-2"
                    >
                      {{ resultadoTeste.sucesso ? 'mdi-check-circle' : 'mdi-alert-circle' }}
                    </v-icon>
                    <div>
                      <strong>{{ resultadoTeste.sucesso ? 'Preço encontrado!' : 'Erro na extração!' }}</strong>
                      <div>{{ resultadoTeste.mensagem }}</div>
                    </div>
                  </div>
                </v-sheet>
              </v-expand-transition>
            </v-card-text>
          </v-tab-item>
          
          <!-- Aba 3: Configurações -->
          <v-tab-item>
            <v-card-text class="pa-6">
              <v-row>
                <v-col cols="12">
                  <v-switch
                    v-model="produto.verificacao_manual"
                    label="Verificação Manual"
                    color="warning"
                    hide-details="auto"
                  ></v-switch>
                  <div class="caption text-grey ml-12 mt-1">
                    Se ativado, o produto não será verificado automaticamente pelo sistema.
                  </div>
                </v-col>
                
                <v-col cols="12">
                  <v-switch
                    v-model="produto.produto_cliente"
                    label="Produto Cliente Base"
                    color="primary"
                    hide-details="auto"
                    :disabled="produto.tipo_produto !== 'cliente'"
                  ></v-switch>
                  <div class="caption text-grey ml-12 mt-1">
                    Marca este produto como base para comparações de preço. Apenas produtos do tipo cliente podem ser marcados como base.
                  </div>
                </v-col>
                
                <v-col cols="12" class="mt-4">
                  <v-alert
                    type="info"
                    outlined
                    icon="mdi-information-outline"
                  >
                    <div class="text-subtitle-2 mb-2">Programação de Verificação</div>
                    <p class="mb-0">Este produto será verificado automaticamente de acordo com a programação do sistema. 
                    A frequência padrão é diária, mas você pode alterar isso nas configurações de agendamento.</p>
                  </v-alert>
                </v-col>
              </v-row>
            </v-card-text>
          </v-tab-item>
        </v-tabs-items>
        
        <v-divider></v-divider>
        
        <!-- Botões de ação -->
        <v-card-actions class="pa-4">
          <v-btn
            text
            color="grey darken-1"
            @click="$router.go(-1)"
          >
            Cancelar
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            v-if="!isLastTab"
            color="primary"
            @click="nextTab"
          >
            Próximo
            <v-icon right>mdi-arrow-right</v-icon>
          </v-btn>
          <v-btn
            v-if="isLastTab"
            color="success"
            type="submit"
            :loading="loading"
            :disabled="!valid || loading"
          >
            <v-icon left>{{ isEditMode ? 'mdi-content-save' : 'mdi-plus-circle' }}</v-icon>
            {{ isEditMode ? 'Atualizar Produto' : 'Adicionar Produto' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
    
    <!-- Snackbar para mensagens -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
      bottom
      right
    >
      {{ snackbar.text }}
      <template v-slot:action="{ attrs }">
        <v-btn
          text
          v-bind="attrs"
          @click="snackbar.show = false"
        >
          Fechar
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()
const store = useStore()

// Estado do formulário
const form = ref(null)
const valid = ref(false)
const loading = ref(false)
const loadingPlataformas = ref(false)
const loadingGrupos = ref(false)
const testandoSeletor = ref(false)
const activeTab = ref(0)
const resultadoTeste = ref(null)

// Lista de plataformas e grupos
const plataformas = ref([])
const grupos = ref([])
const dominiosDisponiveis = ref([])
const dominioSelecionado = ref(null)

// Tipos de produto disponíveis
const tiposProduto = [
  { texto: 'Produto do Cliente', valor: 'cliente' },
  { texto: 'Produto de Concorrente', valor: 'concorrente' }
]

// Dados do produto
const produto = ref({
  nome: '',
  concorrente: '',
  url: '',
  tipo_produto: 'concorrente',
  plataforma: null,
  grupo: null,
  verificacao_manual: false,
  produto_cliente: false,
  preco_cliente: null
})

// Notificações
const snackbar = ref({
  show: false,
  text: '',
  color: 'success',
  timeout: 4000
})

// Detecta se é modo de edição ou criação
const isEditMode = computed(() => !!route.params.id)

// Verifica se é a última aba
const isLastTab = computed(() => activeTab.value === 2)

// Navegar para próxima aba
const nextTab = () => {
  if (activeTab.value < 2) {
    activeTab.value += 1
  }
}

// Abrir URL em nova aba
const abrirUrlPrevia = () => {
  if (produto.value.url) {
    window.open(produto.value.url, '_blank')
  }
}

// Extrair domínio da URL
const extrairDominio = (url) => {
  if (!url) return null
  try {
    const urlObj = new URL(url)
    return urlObj.hostname
  } catch (e) {
    return null
  }
}

// Testar seletor
const testarSeletor = async () => {
  if (!produto.value.url || !produto.value.plataforma?.seletor_css) {
    mostrarSnackbar('URL ou seletor CSS não definidos', 'error')
    return
  }
  
  testandoSeletor.value = true
  resultadoTeste.value = null
  
  try {
    // Endpoint fictício para testar extração - idealmente você criaria este endpoint no backend
    const response = await api.post('testes/extrator/', {
      url: produto.value.url,
      seletor: produto.value.plataforma.seletor_css
    })
    
    if (response.data.preco) {
      resultadoTeste.value = {
        sucesso: true,
        mensagem: `Preço extraído com sucesso: R$ ${response.data.preco.toFixed(2)}`
      }
    } else {
      resultadoTeste.value = {
        sucesso: false,
        mensagem: 'Não foi possível extrair o preço com este seletor.'
      }
    }
  } catch (error) {
    console.error('Erro ao testar seletor:', error)
    resultadoTeste.value = {
      sucesso: false,
      mensagem: 'Erro ao testar seletor: ' + (error.response?.data?.detail || error.message)
    }
  } finally {
    testandoSeletor.value = false
  }
}

// Carregar dados iniciais
onMounted(async () => {
  try {
    await Promise.all([carregarPlataformas(), carregarGrupos()])
    
    if (isEditMode.value) {
      await carregarProduto(route.params.id)
    } else {
      // Aplicar grupo automaticamente para novos produtos
      await aplicarGrupoUsuario()
    }
  } catch (error) {
    console.error('Erro ao carregar dados iniciais:', error)
    mostrarSnackbar('Erro ao carregar dados necessários. Por favor, tente novamente.', 'error')
  }
})

// Carregar plataformas disponíveis
const carregarPlataformas = async () => {
  loadingPlataformas.value = true
  try {
    console.log('Carregando plataformas...')
    const response = await api.get('plataformas/')
    console.log('Resposta plataformas:', response.data)
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
    console.log('Carregando grupos...')
    // Obter o cliente atual do usuário
    const userInfo = await api.get('user/info/')
    console.log('User info:', userInfo.data)
    
    if (userInfo.data.cliente_atual) {
      // Carregar apenas grupos associados ao cliente atual
      const response = await api.get(`grupos/?cliente=${userInfo.data.cliente_atual}`)
      console.log('Grupos response:', response.data)
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

// Função para obter e aplicar o grupo do usuário ao produto
const aplicarGrupoUsuario = async () => {
  try {
    console.log('Aplicando grupo do usuário...')
    // Obter informações do usuário
    const userInfo = await api.get('user/info/')
    console.log('User info para aplicar grupo:', userInfo.data)
    
    // Obter grupos vinculados ao cliente atual do usuário
    if (userInfo.data.cliente_atual) {
      // Carregar grupos associados ao cliente atual
      const gruposResponse = await api.get(`grupos/?cliente=${userInfo.data.cliente_atual}`);
      console.log('Grupos para aplicar:', gruposResponse.data)
      
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

// Carregar dados do produto para edição
const carregarProduto = async (id) => {
  loading.value = true
  try {
    console.log(`Carregando produto ${id}...`)
    const response = await api.get(`produtos/${id}/`)
    produto.value = response.data
    
    // Se for um produto do cliente, garantir que as propriedades específicas estejam definidas
    if (produto.value.tipo_produto === 'cliente' && produto.value.preco_cliente === null) {
      produto.value.preco_cliente = 0
    }
    
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
      const userInfo = await api.get('user/info/')
      
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
      
      // Se for produto do cliente, garantir que o preço está definido
      if (produto.value.tipo_produto === 'cliente' && produto.value.preco_cliente === null) {
        produto.value.preco_cliente = 0
      }
      
      // Se for produto marcado como cliente base, garantir que o tipo é cliente
      if (produto.value.produto_cliente && produto.value.tipo_produto !== 'cliente') {
        produto.value.tipo_produto = 'cliente'
      }
      
      // Cria uma cópia do produto com apenas os campos necessários e garantindo que IDs sejam usados
      const produtoParaEnviar = {
        nome: produto.value.nome,
        concorrente: produto.value.concorrente,
        url: produto.value.url,
        verificacao_manual: produto.value.verificacao_manual || false,
        tipo_produto: produto.value.tipo_produto || 'concorrente',
        produto_cliente: produto.value.produto_cliente || false,
        cliente: clienteId  // Usar o ID do cliente
      }
      
      // Adicionar campos condicionais
      if (grupoId) {
        produtoParaEnviar.grupo = grupoId
      }
      
      if (plataformaId) {
        produtoParaEnviar.plataforma = plataformaId
      }
      
      if (produto.value.tipo_produto === 'cliente' && produto.value.preco_cliente !== null) {
        produtoParaEnviar.preco_cliente = parseFloat(produto.value.preco_cliente)
      }
      
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
      
      // Se estiver marcando como produto_cliente=true, verificar se já existem outros com o mesmo nome
      if (produtoParaEnviar.produto_cliente) {
        try {
          // Obter produtos com o mesmo nome
          const produtosResponse = await api.get(`produtos/?nome=${produtoParaEnviar.nome}&cliente=${clienteId}`)
          const produtosDoMesmoNome = produtosResponse.data.results || []
          
          // Filtrar apenas os que estão marcados como produto_cliente
          const produtosClienteBase = produtosDoMesmoNome.filter(p => 
            p.produto_cliente === true && 
            (isEditMode.value ? p.id !== produto.value.id : true)
          )
          
          // Se encontrar outros produtos marcados como base, confirmar com o usuário
          if (produtosClienteBase.length > 0) {
            // Perguntar ao usuário usando o snackbar (não ideal, mas funcionará)
            mostrarSnackbar(
              `Já existe outro produto "${produtoParaEnviar.nome}" marcado como base. Este será desmarcado automaticamente.`,
              'info',
              5000
            )
            // Aqui não precisamos desmarcar manualmente, pois o backend já fará isso
          }
        } catch (err) {
          console.error('Erro ao verificar outros produtos marcados como base:', err)
          // Continuar mesmo se houver falha aqui
        }
      }
      
      console.log('Enviando produto:', produtoParaEnviar)
      let response;
      if (isEditMode.value) {
        response = await api.put(`produtos/${produto.value.id}/`, produtoParaEnviar)
        mostrarSnackbar('Produto atualizado com sucesso')
      } else {
        response = await api.post('produtos/', produtoParaEnviar)
        mostrarSnackbar('Produto adicionado com sucesso')
      }
      
      // Redirecionar para a lista de produtos após um breve delay
      setTimeout(() => {
        router.push('/products')
      }, 1000)
      
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
const mostrarSnackbar = (text, color = 'success', timeout = 4000) => {
  snackbar.value = {
    show: true,
    text,
    color,
    timeout
  }
}

// Observar mudanças na URL para atualizar o domínio
watch(() => produto.value.url, (newUrl) => {
  const dominio = extrairDominio(newUrl)
  if (dominio) {
    dominioSelecionado.value = { nome: dominio }
    dominiosDisponiveis.value = [{ nome: dominio }]
    
    // Tentar encontrar uma plataforma correspondente ao domínio
    if (plataformas.value.length > 0 && !produto.value.plataforma) {
      const plataformaEncontrada = plataformas.value.find(
        p => p.nome.toLowerCase().includes(dominio.toLowerCase()) || 
             dominio.toLowerCase().includes(p.nome.toLowerCase())
      )
      
      if (plataformaEncontrada) {
        produto.value.plataforma = plataformaEncontrada
        mostrarSnackbar('Plataforma selecionada automaticamente com base no domínio', 'info')
      }
    }
  } else {
    dominioSelecionado.value = null
    dominiosDisponiveis.value = []
  }
})
</script>

<style scoped>
.gradient-header {
  background: linear-gradient(135deg, var(--v-primary-base) 0%, var(--v-primary-darken1) 100%);
  border-radius: 8px;
}

.form-card {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.v-tabs-bar) {
  border-radius: 8px 8px 0 0;
}

:deep(.v-tabs) .v-tab {
  text-transform: none !important;
  letter-spacing: normal !important;
  font-weight: 500 !important;
  font-size: 1rem !important;
}

:deep(.v-input--is-disabled) {
  opacity: 0.7;
}
</style>