<template>
  <v-container fluid>
    <!-- Cabeçalho da página com visual aprimorado -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="2" class="mb-6 gradient-header">
          <v-card-text>
            <div class="d-flex flex-wrap align-center">
              <div>
                <h1 class="text-h4 font-weight-bold white--text mb-1">Dashboard</h1>
                <p class="text-subtitle-1 white--text mb-0">Monitore seus produtos e concorrentes</p>
              </div>
              <v-spacer></v-spacer>
              <v-btn
                color="white"
                class="primary--text text-none px-4 elevation-1"
                @click="$router.push('/products/add')"
              >
                <v-icon left>mdi-plus</v-icon>
                Adicionar Produto
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Cards de informações com visual aprimorado -->
    <v-row>
      <v-col cols="12" md="4">
        <v-card class="mb-4 stats-card" elevation="3" rounded="lg">
          <v-card-text class="pa-4">
            <div class="d-flex align-center">
              <div class="rounded-circle primary pa-4 mr-4">
                <v-icon color="white" size="32">mdi-package-variant-closed</v-icon>
              </div>
              <div>
                <div class="text-overline text-grey">Total de Produtos</div>
                <div class="text-h4 font-weight-bold">{{ produtosUnicos.length }}</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card class="mb-4 stats-card" elevation="3" rounded="lg">
          <v-card-text class="pa-4">
            <div class="d-flex align-center">
              <div class="rounded-circle info pa-4 mr-4">
                <v-icon color="white" size="32">mdi-account-group</v-icon>
              </div>
              <div>
                <div class="text-overline text-grey">Concorrentes</div>
                <div class="text-h4 font-weight-bold">{{ concorrentesUnicos.length }}</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card class="mb-4 stats-card" elevation="3" rounded="lg">
          <v-card-text class="pa-4">
            <div class="d-flex align-center">
              <div class="rounded-circle success pa-4 mr-4">
                <v-icon color="white" size="32">mdi-compare</v-icon>
              </div>
              <div>
                <div class="text-overline text-grey">Comparações</div>
                <div class="text-h4 font-weight-bold">{{ produtos.length }}</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Conteúdo principal com visual aprimorado -->
    <v-card class="rounded-lg" elevation="3">
      <v-toolbar flat class="primary lighten-1" dark>
        <v-toolbar-title>
          <v-icon left>mdi-compare-horizontal</v-icon>
          Comparação de Produtos
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Pesquisar produto"
          hide-details
          dense
          class="mt-2 mr-4"
          style="max-width: 300px;"
          outlined
          dark
          color="white"
          single-line
        ></v-text-field>
        <v-btn
          icon
          :loading="loading"
          @click="carregarDados"
          color="white"
          class="ml-2"
        >
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </v-toolbar>
      
      <!-- Estado de carregamento -->
      <v-progress-linear
        indeterminate
        v-if="loading"
        color="primary"
      ></v-progress-linear>
      
      <!-- Conteúdo da tabela -->
      <v-card-text class="pa-4">
        <div v-if="produtosAgrupados.length === 0 && !loading" class="text-center pa-8">
          <v-img
            src="@/assets/empty-products.svg"
            max-width="200"
            class="mx-auto mb-4"
            alt="Nenhum produto encontrado"
          ></v-img>
          <h3 class="text-h5 grey--text text--darken-1 mt-4">Nenhum produto encontrado</h3>
          <p class="text-body-1 grey--text mb-6">Comece adicionando produtos usando o botão no topo da página</p>
          <v-btn
            color="primary"
            @click="$router.push('/products/add')"
          >
            <v-icon left>mdi-plus</v-icon>
            Adicionar Produto
          </v-btn>
        </div>
        
        <!-- Lista de grupos de produtos filtrados -->
        <div v-if="produtosAgrupadosFiltrados.length > 0">
          <div
            v-for="(grupo, index) in produtosAgrupadosFiltrados"
            :key="index"
            class="mb-5 produto-grupo"
          >
            <!-- Cabeçalho do grupo com visual aprimorado -->
            <div 
              class="d-flex align-center pa-4 grupo-header"
              @click="toggleGrupo(index)"
              :class="{'grupo-header-active': gruposAbertos.includes(index)}"
            >
              <v-icon class="mr-2 transition-swing" :class="{'transform-rotate-90': gruposAbertos.includes(index)}">
                mdi-chevron-right
              </v-icon>
              
              <!-- Nome do produto -->
              <span class="text-subtitle-1 font-weight-bold">{{ grupo.nome }}</span>
              
              <!-- Mensagem quando não houver produto cliente definido -->
              <v-chip
                v-if="!grupo.produtoClienteBase"
                small
                outlined
                color="warning"
                class="ml-3"
              >
                <v-icon left size="16">mdi-alert-circle</v-icon>
                Por favor, defina o produto cliente
              </v-chip>
              
              <v-spacer></v-spacer>
              
              <!-- Resumo do produto (apenas se houver produto cliente base) -->
              <template v-if="grupo.produtoClienteBase">
                <div class="d-none d-md-flex align-center">
                  <!-- Preço do cliente -->
                  <div class="text-center mx-3 resumo-grupo">
                    <div class="caption grey--text">Preço Cliente</div>
                    <div class="subtitle-1 font-weight-medium primary--text">
                      {{ 
                        grupo.produtoClienteBase.preco_cliente ? 
                        formatarPreco(grupo.produtoClienteBase.preco_cliente) : 
                        'N/A' 
                      }}
                    </div>
                  </div>
                  
                  <!-- Menor preço concorrente -->
                  <div class="text-center mx-3 resumo-grupo">
                    <div class="caption grey--text">Menor Preço</div>
                    <div class="subtitle-1 font-weight-medium">
                      {{ 
                        grupo.menorPrecoConcorrente ? 
                        formatarPreco(grupo.menorPrecoConcorrente) : 
                        'N/A' 
                      }}
                    </div>
                  </div>
                  
                  <!-- Diferença percentual -->
                  <div class="text-center mx-3" v-if="grupo.diferencaPercentual !== null">
                    <div class="caption grey--text">Variação</div>
                    <v-chip
                      small
                      :color="getCorDiferenca(grupo.diferencaPercentual)"
                      dark
                    >
                      {{ formatarPercentual(grupo.diferencaPercentual) }}
                    </v-chip>
                  </div>
                  
                  <!-- Concorrente com menor preço -->
                  <div class="text-center mx-3" v-if="grupo.concorrenteMenorPreco">
                    <div class="caption grey--text">Concorrente</div>
                    <div class="subtitle-2 font-weight-regular text-truncate" style="max-width: 150px">
                      {{ grupo.concorrenteMenorPreco }}
                    </div>
                  </div>
                </div>
              </template>
            </div>
            
            <!-- Conteúdo do grupo (tabela de produtos) -->
            <div v-if="gruposAbertos.includes(index)" class="pa-4 grupo-content">
              <v-data-table
                :headers="headers"
                :items="grupo.produtos"
                :items-per-page="5"
                class="elevation-0 product-table"
                hide-default-footer
                dense
              >
                <!-- Tipo de produto -->
                <template v-slot:item.tipo_produto="{ item }">
                  <v-chip
                    :color="item.tipo_produto === 'cliente' ? 'primary' : 'grey lighten-3'"
                    small
                    :text-color="item.tipo_produto === 'cliente' ? 'white' : 'grey darken-2'"
                  >
                    {{ item.tipo_produto === 'cliente' ? 'Cliente' : 'Concorrente' }}
                  </v-chip>
                </template>
                
                <!-- Concorrente -->
                <template v-slot:item.concorrente="{ item }">
                  <span :class="{'font-weight-bold': item.tipo_produto === 'cliente'}">
                    {{ item.concorrente }}
                    <span v-if="item.produto_cliente" class="ml-1 caption font-italic">(Produto Cliente)</span>
                  </span>
                </template>
                
                <!-- Produto Cliente Base -->
                <template v-slot:item.produto_cliente="{ item }">
                  <v-icon v-if="item.produto_cliente" color="primary">mdi-star</v-icon>
                  <v-icon v-else color="grey lighten-1">mdi-star-outline</v-icon>
                </template>
                
                <!-- Preço -->
                <template v-slot:item.preco="{ item }">
                  <span :class="{'primary--text font-weight-bold': item.produto_cliente}">
                    {{ getPreco(item) }}
                  </span>
                </template>
                
                <!-- Diferença percentual -->
                <template v-slot:item.diferenca_percentual="{ item }">
                  <v-chip
                    v-if="item.diferenca_percentual !== null"
                    :color="getCorDiferenca(item.diferenca_percentual)"
                    small
                    dark
                  >
                    {{ formatarPercentual(item.diferenca_percentual) }}
                  </v-chip>
                  <span v-else class="text-caption grey--text">N/A</span>
                </template>
                
                <!-- Data da verificação -->
                <template v-slot:item.ultima_verificacao="{ item }">
                  <div class="d-flex align-center">
                    <v-icon small class="mr-1" :color="item.ultima_verificacao ? 'success' : 'grey'">
                      {{ item.ultima_verificacao ? 'mdi-clock-check-outline' : 'mdi-clock-alert-outline' }}
                    </v-icon>
                    <span class="text-caption">{{ formatDate(item.ultima_verificacao) }}</span>
                  </div>
                </template>
                
                <!-- Ações -->
                <template v-slot:item.actions="{ item }">
                  <div class="d-flex">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          icon
                          x-small
                          color="primary"
                          class="mr-1"
                          @click="verDetalhes(item.id)"
                          v-bind="attrs"
                          v-on="on"
                        >
                          <v-icon>mdi-eye</v-icon>
                        </v-btn>
                      </template>
                      <span>Ver detalhes</span>
                    </v-tooltip>
                    
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          icon
                          x-small
                          color="success"
                          @click="verificarPreco(item.id)"
                          :loading="verificandoItem === item.id"
                          v-bind="attrs"
                          v-on="on"
                        >
                          <v-icon>mdi-refresh</v-icon>
                        </v-btn>
                      </template>
                      <span>Verificar preço</span>
                    </v-tooltip>
                    
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          icon
                          x-small
                          color="warning"
                          class="ml-1"
                          @click="definirProdutoClienteBase(item)"
                          :disabled="item.produto_cliente"
                          v-bind="attrs"
                          v-on="on"
                        >
                          <v-icon>mdi-star</v-icon>
                        </v-btn>
                      </template>
                      <span>Definir como produto cliente base</span>
                    </v-tooltip>
                  </div>
                </template>
              </v-data-table>
            </div>
          </div>
        </div>

        <!-- Mensagem quando o filtro não encontrar resultados -->
        <div v-if="produtosAgrupados.length > 0 && produtosAgrupadosFiltrados.length === 0" class="text-center pa-6">
          <v-icon size="48" color="grey lighten-1">mdi-file-search-outline</v-icon>
          <h3 class="text-h6 grey--text text--darken-1 mt-3">Nenhum produto corresponde à sua pesquisa</h3>
        </div>
      </v-card-text>
    </v-card>
    
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import api from '@/services/api'

const router = useRouter()
const store = useStore()
const loading = ref(false)
const produtos = ref([])
const debug = ref(false)
const verificandoItem = ref(null)
const gruposAbertos = ref([])
const search = ref('') // Campo de pesquisa

// Estado para snackbar
const snackbar = ref({
  show: false,
  text: '',
  color: 'success',
  timeout: 3000
})

// Função para alternar a exibição de um grupo
const toggleGrupo = (index) => {
  const currentIndex = gruposAbertos.value.indexOf(index)
  if (currentIndex === -1) {
    gruposAbertos.value.push(index)
  } else {
    gruposAbertos.value.splice(currentIndex, 1)
  }
}

// Cabeçalhos da tabela
const headers = [
  { text: 'Tipo', value: 'tipo_produto', width: '100px' },
  { text: 'Base', value: 'produto_cliente', width: '80px', align: 'center' },
  { text: 'Empresa', value: 'concorrente' },
  { text: 'Preço', value: 'preco', width: '120px' },
  { text: 'Diferença', value: 'diferenca_percentual', width: '120px' },
  { text: 'Última Verificação', value: 'ultima_verificacao', width: '180px' },
  { text: 'Ações', value: 'actions', align: 'center', sortable: false, width: '140px' }
]

// Produtos únicos (pelo nome)
const produtosUnicos = computed(() => {
  const nomes = new Set()
  const unicos = []
  
  produtos.value.forEach(produto => {
    if (!nomes.has(produto.nome)) {
      nomes.add(produto.nome)
      unicos.push(produto)
    }
  })
  
  return unicos
})

// Concorrentes únicos
const concorrentesUnicos = computed(() => {
  const nomes = new Set()
  produtos.value.forEach(p => {
    if (p.tipo_produto === 'concorrente' && p.concorrente) {
      nomes.add(p.concorrente)
    }
  })
  return Array.from(nomes)
})

// Produtos agrupados por nome
const produtosAgrupados = computed(() => {
  const grupos = []
  const nomesProdutos = new Set()
  
  // Coletar nomes únicos
  produtos.value.forEach(p => nomesProdutos.add(p.nome))
  
  // Para cada nome, criar um grupo
  Array.from(nomesProdutos).forEach(nome => {
    const produtosDesseTipo = produtos.value.filter(p => p.nome === nome)
    
    // Produto cliente base (marcado como produto_cliente)
    const produtoClienteBase = produtosDesseTipo.find(p => p.produto_cliente === true)
    
    // Produtos concorrentes
    const produtosConcorrentes = produtosDesseTipo.filter(p => p.tipo_produto === 'concorrente')
    
    // Encontrar menor preço entre concorrentes
    let menorPrecoConcorrente = null
    let concorrenteMenorPreco = null
    
    if (produtosConcorrentes.length > 0) {
      // Filtrar produtos concorrentes com preços válidos
      const concorrentesComPreco = produtosConcorrentes.filter(p => {
        const preco = p.preco_ultimo || p.menor_preco_concorrente
        return preco !== null && preco !== undefined && !isNaN(preco) && preco > 0
      })
      
      if (concorrentesComPreco.length > 0) {
        // Encontrar o com menor preço
        let menorPreco = Number.MAX_SAFE_INTEGER
        let produtoMenorPreco = null
        
        concorrentesComPreco.forEach(p => {
          const preco = p.preco_ultimo || p.menor_preco_concorrente
          if (preco < menorPreco) {
            menorPreco = preco
            produtoMenorPreco = p
          }
        })
        
        menorPrecoConcorrente = menorPreco
        concorrenteMenorPreco = produtoMenorPreco?.concorrente
        
        console.log(`Menor preço para ${nome}: ${menorPrecoConcorrente} (${concorrenteMenorPreco})`)
      }
    }
    
    // Se não tiver produto cliente base, usar qualquer produto do cliente
    let produtoClienteExibicao = produtoClienteBase
    if (!produtoClienteExibicao) {
      produtoClienteExibicao = produtosDesseTipo.find(p => p.tipo_produto === 'cliente')
    }
    
    // Calcular diferença percentual
    let diferencaPercentual = null
    if (produtoClienteExibicao && 
        produtoClienteExibicao.preco_cliente && 
        !isNaN(produtoClienteExibicao.preco_cliente) && 
        menorPrecoConcorrente && 
        !isNaN(menorPrecoConcorrente)) {
      
      diferencaPercentual = ((produtoClienteExibicao.preco_cliente - menorPrecoConcorrente) / menorPrecoConcorrente) * 100
      diferencaPercentual = Math.round(diferencaPercentual * 10) / 10
    }
    
    // Processar cada produto para exibição na tabela
    const produtosProcessados = produtosDesseTipo.map(p => {
      let diferencaIndividual = null
      
      // Para produtos do cliente, calcular a diferença em relação ao menor preço concorrente
      if (p.tipo_produto === 'cliente' && p.preco_cliente && menorPrecoConcorrente) {
        diferencaIndividual = ((p.preco_cliente - menorPrecoConcorrente) / menorPrecoConcorrente) * 100
        diferencaIndividual = Math.round(diferencaIndividual * 10) / 10
      }
      
      // Para produtos concorrentes, calcular a diferença em relação ao produto cliente base
      if (p.tipo_produto === 'concorrente' && produtoClienteExibicao && produtoClienteExibicao.preco_cliente) {
        const precoConcorrente = p.preco_ultimo || p.menor_preco_concorrente
        if (precoConcorrente) {
          diferencaIndividual = ((precoConcorrente - produtoClienteExibicao.preco_cliente) / produtoClienteExibicao.preco_cliente) * 100
          diferencaIndividual = Math.round(diferencaIndividual * 10) / 10
        }
      }
      
      return {
        ...p,
        preco_exibicao: p.tipo_produto === 'cliente' 
          ? p.preco_cliente 
          : (p.preco_ultimo || p.menor_preco_concorrente),
        diferenca_percentual: diferencaIndividual
      }
    })
    
    grupos.push({
      nome,
      produtos: produtosProcessados,
      produtoClienteBase: produtoClienteExibicao,
      menorPrecoConcorrente,
      concorrenteMenorPreco,
      diferencaPercentual
    })
  })
  
  // Ordenar grupos pela presença de um produto cliente base primeiro
  return grupos.sort((a, b) => {
    // Priorizar grupos com produto cliente base
    if (a.produtoClienteBase && !b.produtoClienteBase) return -1
    if (!a.produtoClienteBase && b.produtoClienteBase) return 1
    // Em seguida, ordenar alfabeticamente pelo nome
    return a.nome.localeCompare(b.nome)
  })
})

// Produtos filtrados com base na pesquisa
const produtosAgrupadosFiltrados = computed(() => {
  if (!search.value) return produtosAgrupados.value
  
  const searchTerm = search.value.toLowerCase().trim()
  
  return produtosAgrupados.value.filter(grupo => {
    // Verifica se o nome do grupo contém o termo de pesquisa
    if (grupo.nome.toLowerCase().includes(searchTerm)) return true
    
    // Verifica se algum produto deste grupo contém o termo de pesquisa
    return grupo.produtos.some(produto => 
      produto.nome.toLowerCase().includes(searchTerm) || 
      produto.concorrente.toLowerCase().includes(searchTerm)
    )
  })
})

// Exibir mensagem no snackbar
const mostrarSnackbar = (texto, cor = 'success', timeout = 3000) => {
  snackbar.value = {
    show: true,
    text: texto,
    color: cor,
    timeout: timeout
  }
}

// Função para definir um produto como cliente base
const definirProdutoClienteBase = async (produto) => {
  try {
    console.log(`Iniciando atualização do produto ${produto.id} para cliente base`);
    
    // Verificar se existe um cliente atual selecionado
    if (!store.getters['auth/user']?.cliente_atual) {
      mostrarSnackbar('Por favor, selecione um cliente atual no menu superior antes de continuar', 'warning');
      return;
    }
    
    // Obter o ID do cliente atual
    const clienteId = typeof store.getters['auth/user'].cliente_atual === 'object' 
      ? store.getters['auth/user'].cliente_atual.id 
      : store.getters['auth/user'].cliente_atual;
      
    console.log('Cliente atual ID:', clienteId);
    
    // Obter o grupo do produto
    const grupoId = typeof produto.grupo === 'object' 
      ? produto.grupo.id 
      : produto.grupo;
      
    console.log('Grupo ID:', grupoId);
    
    // Encontrar outros produtos com o mesmo nome que já estão marcados como produto_cliente
    const produtosDoMesmoNome = produtos.value.filter(p => 
      p.nome === produto.nome && 
      p.id !== produto.id && 
      p.produto_cliente === true
    );
    
    // Se encontrar outros produtos marcados como base, desmarcar eles antes
    if (produtosDoMesmoNome.length > 0) {
      console.log(`Encontrados ${produtosDoMesmoNome.length} produtos com o mesmo nome marcados como cliente base. Desmarcando...`);
      
      // Para cada produto encontrado, desmarcar como produto_cliente
      for (const produtoAnterior of produtosDoMesmoNome) {
        try {
          await api.patch(`/produtos/${produtoAnterior.id}/`, {
            produto_cliente: false,
            cliente: clienteId,
            grupo: grupoId
          });
          
          // Atualizar localmente
          const idx = produtos.value.findIndex(p => p.id === produtoAnterior.id);
          if (idx !== -1) {
            produtos.value[idx].produto_cliente = false;
          }
          
          console.log(`Produto ${produtoAnterior.id} desmarcado como cliente base`);
        } catch (err) {
          console.error(`Erro ao desmarcar produto ${produtoAnterior.id}:`, err);
        }
      }
    }
    
    // Preparar os dados de atualização
    const dadosAtualizacao = {
      produto_cliente: true,
      cliente: clienteId,
      grupo: grupoId,
    };
    
    // Se o produto for do tipo concorrente, alterá-lo para cliente
    if (produto.tipo_produto === 'concorrente') {
      dadosAtualizacao.tipo_produto = 'cliente';
      console.log('Alterando o tipo do produto de concorrente para cliente:', dadosAtualizacao);
    }
    
    console.log('Dados de atualização completos:', dadosAtualizacao);
    
    // Atualizar o produto com o novo status
    const response = await api.patch(`/produtos/${produto.id}/`, dadosAtualizacao);
    
    console.log('Atualização concluída com sucesso', response.data);
    
    // Atualizar localmente o produto antes de recarregar tudo
    const produtoIndex = produtos.value.findIndex(p => p.id === produto.id);
    if (produtoIndex !== -1) {
      produtos.value[produtoIndex].produto_cliente = true;
      produtos.value[produtoIndex].tipo_produto = 'cliente';
      console.log('Produto atualizado localmente antes de recarregar dados');
    }
    
    // Recarregar dados após a atualização
    await carregarDados();
    
    mostrarSnackbar('Produto definido como base para comparações');
    
  } catch (error) {
    console.error('Erro ao definir produto cliente base:', error);
    
    if (error.response) {
      console.error('Detalhes do erro:', error.response.data);
      
      if (error.response.status === 400) {
        let mensagemErro = '';
        if (typeof error.response.data === 'object') {
          for (const campo in error.response.data) {
            mensagemErro += `${campo}: ${error.response.data[campo].join(', ')}. `;
          }
        } else {
          mensagemErro = error.response.data.detail || 'Erro na validação dos dados.';
        }
        mostrarSnackbar(`Erro: ${mensagemErro}`, 'error');
      } 
      else if (error.response.status === 403) {
        mostrarSnackbar('Este produto não pertence ao cliente atual selecionado.', 'error');
      }
      else {
        mostrarSnackbar(`Erro ao definir produto cliente base: ${error.response.data.detail || 'Erro interno do servidor'}`, 'error');
      }
    } else {
      mostrarSnackbar('Erro de conexão ao tentar atualizar o produto', 'error');
    }
  }
}

// Função para obter o preço do produto (cliente ou concorrente)
const getPreco = (produto) => {
  // Para produtos do cliente
  if (produto.tipo_produto === 'cliente') {
    // Verificar se preco_cliente existe e é válido
    if (produto.preco_cliente !== null && produto.preco_cliente !== undefined && 
        !isNaN(produto.preco_cliente) && produto.preco_cliente > 0) {
      return formatarPreco(produto.preco_cliente);
    }
    
    // Caso não tenha, verificar preco_ultimo
    if (produto.preco_ultimo !== null && produto.preco_ultimo !== undefined && 
        !isNaN(produto.preco_ultimo) && produto.preco_ultimo > 0) {
      return formatarPreco(produto.preco_ultimo);
    }
    
    // Se não tiver nenhum, mostrar placeholder
    return 'Preço não definido';
  } 
  // Para produtos concorrentes
  else {
    // Verificar preco_ultimo (do histórico)
    if (produto.preco_ultimo !== null && produto.preco_ultimo !== undefined && 
        !isNaN(produto.preco_ultimo) && produto.preco_ultimo > 0) {
      return formatarPreco(produto.preco_ultimo);
    }
    
    // Verificar menor_preco_concorrente
    if (produto.menor_preco_concorrente !== null && produto.menor_preco_concorrente !== undefined && 
        !isNaN(produto.menor_preco_concorrente) && produto.menor_preco_concorrente > 0) {
      return formatarPreco(produto.menor_preco_concorrente);
    }
    
    // Se não tiver nenhum, mostrar placeholder
    return 'Preço não verificado';
  }
}

// Formatação de preço
const formatarPreco = (valor) => {
  if (valor === null || valor === undefined || isNaN(valor)) {
    return 'N/A';
  }
  
  // Garantir que seja tratado como número
  const numero = Number(valor);
  if (isNaN(numero)) {
    return 'N/A';
  }
  
  return `R$ ${numero.toFixed(2).replace('.', ',')}`;
}

// Formatação de percentual
const formatarPercentual = (valor) => {
  if (valor === null || valor === undefined || isNaN(valor)) {
    return 'N/A';
  }
  
  // Garantir que seja tratado como número
  const numero = Number(valor);
  if (isNaN(numero)) {
    return 'N/A';
  }
  
  const sinal = numero > 0 ? '+' : '';
  return `${sinal}${numero.toFixed(1).replace('.', ',')}%`;
}

// Determinar a cor da diferença
const getCorDiferenca = (diferenca) => {
  if (diferenca === null || diferenca === undefined || isNaN(diferenca)) return 'grey'
  return diferenca <= 0 ? 'success' : 'error'
}

// Formatar data
const formatDate = (dateString) => {
  if (!dateString) return 'Nunca verificado'
  try {
    const options = { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }
    return new Date(dateString).toLocaleString('pt-BR', options)
  } catch (error) {
    console.error('Erro ao formatar data:', error)
    return dateString || '-'
  }
}

// Função para carregar dados
const carregarDados = async () => {
  loading.value = true;
  try {
    // Limpar os dados atuais
    produtos.value = [];
    
    // Usar timestamp para evitar cache
    const timestamp = new Date().getTime();
    
    // Buscar produtos
    const produtosResponse = await api.get(`/produtos/?t=${timestamp}`);
    console.log('Resposta da API de produtos:', produtosResponse.data);
    
    if (produtosResponse.data.results && Array.isArray(produtosResponse.data.results)) {
      produtos.value = produtosResponse.data.results;
      console.log('Produtos carregados:', produtos.value.length);
      
      // Para cada produto, recuperar o histórico de preços
      const produtosPromises = produtos.value.map(async (produto) => {
        try {
          // Recuperar histórico usando o endpoint correto
          const historicoResponse = await api.get(`/historico/?produto=${produto.id}&limit=1`);
          
          // Verificar se há resultados e se eles estão no formato esperado
          if (historicoResponse.data && 
              historicoResponse.data.results && 
              historicoResponse.data.results.length > 0) {
            
            // Obter o preço do histórico mais recente
            const precoHistorico = parseFloat(historicoResponse.data.results[0].preco);
            console.log(`Preço do histórico para ${produto.nome}: ${precoHistorico}`);
            
            // Atribuir ao produto
            produto.preco_ultimo = precoHistorico;
            
            // Para produtos do cliente sem preço, usar o do histórico
            if (produto.tipo_produto === 'cliente' && 
                (!produto.preco_cliente || produto.preco_cliente === 0)) {
              produto.preco_cliente = precoHistorico;
              
              // Atualizar no backend
              try {
                await api.patch(`/produtos/${produto.id}/`, {
                  preco_cliente: precoHistorico,
                  cliente: produto.cliente,
                  grupo: produto.grupo
                });
                console.log(`Preço do produto ${produto.id} atualizado no backend`);
              } catch (err) {
                console.error(`Erro ao atualizar preço no backend:`, err);
              }
            }
          } else {
            console.log(`Sem histórico de preço para produto ${produto.id}`);
          }
        } catch (error) {
          console.error(`Erro ao carregar histórico do produto ${produto.id}:`, error);
        }
      });
      
      // Aguardar todas as promessas
      await Promise.all(produtosPromises);
      
      // Abrir o primeiro grupo
      if (produtosAgrupados.value.length > 0 && gruposAbertos.value.length === 0) {
        gruposAbertos.value.push(0);
      }
    } else {
      produtos.value = [];
      console.warn('Nenhum produto retornado da API');
    }
  } catch (error) {
    console.error('Erro ao carregar dados:', error);
    mostrarSnackbar('Erro ao carregar dados', 'error');
  } finally {
    loading.value = false;
  }
}

// Função para verificar preço de um produto
const verificarPreco = async (produtoId) => {
  verificandoItem.value = produtoId
  try {
    await api.post(`/produtos/${produtoId}/verificar/`)
    // Recarregar os dados após verificar o preço
    await carregarDados()
    mostrarSnackbar('Preço verificado com sucesso')
  } catch (error) {
    console.error('Erro ao verificar preço:', error)
    mostrarSnackbar('Erro ao verificar preço', 'error')
  } finally {
    verificandoItem.value = null
  }
}

// Navegar para detalhes do produto
const verDetalhes = (produtoId) => {
  if (produtoId) {
    router.push(`/products/${produtoId}`)
  }
}

// Montar o componente
onMounted(() => {
  carregarDados()
})
</script>

<style scoped>
.gradient-header {
  background: linear-gradient(135deg, var(--v-primary-base) 0%, var(--v-primary-darken1) 100%);
  border-radius: 8px;
}

.stats-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
}

.produto-grupo {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.12);
  transition: box-shadow 0.3s ease;
}

.produto-grupo:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.grupo-header {
  background-color: #f5f5f5;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  transition: background-color 0.2s ease;
  cursor: pointer;
}

.grupo-header:hover {
  background-color: #eeeeee;
}

.grupo-header-active {
  background-color: #e3f2fd; /* Azul claro para destacar o grupo ativo */
}

.grupo-content {
  background-color: white;
}

.transform-rotate-90 {
  transform: rotate(90deg);
}

.resumo-grupo {
  position: relative;
}

.resumo-grupo::after {
  content: "";
  position: absolute;
  right: -18px;
  top: 50%;
  height: 30px;
  border-right: 1px solid rgba(0, 0, 0, 0.12);
  transform: translateY(-50%);
}

.resumo-grupo:last-child::after {
  display: none;
}

.product-table {
  border-radius: 4px;
  overflow: hidden;
}

:deep(.v-data-table th) {
  font-weight: bold !important;
  color: rgba(0, 0, 0, 0.7) !important;
  background-color: #fafafa;
}

:deep(.v-data-table tr:hover) {
  background-color: #f5f7fa !important;
}

:deep(.v-data-table tr:nth-child(even)) {
  background-color: #fcfcfc;
}

.rounded-circle {
  border-radius: 50% !important;
}
</style>