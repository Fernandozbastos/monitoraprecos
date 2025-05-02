<template>
  <v-container fluid>
    <!-- Botão de navegação com melhor visual -->
    <v-row>
      <v-col cols="12">
        <v-btn 
          text 
          class="mb-4 pl-0 transition-swing"
          @click="$router.go(-1)"
        >
          <v-icon left>mdi-arrow-left</v-icon>
          Voltar para a lista
        </v-btn>
      </v-col>
    </v-row>

    <!-- Estado de carregamento aprimorado -->
    <v-row v-if="loading">
      <v-col cols="12" class="d-flex justify-center align-center py-12">
        <div class="text-center">
          <v-progress-circular
            indeterminate
            color="primary"
            size="64"
          ></v-progress-circular>
          <div class="mt-4 text-subtitle-1 grey--text">Carregando detalhes do produto...</div>
        </div>
      </v-col>
    </v-row>
    
    <template v-else>
      <!-- Cabeçalho do produto -->
      <v-row>
        <v-col cols="12">
          <v-card elevation="3" class="mb-6 gradient-header">
            <v-card-text class="pa-6">
              <div class="d-flex flex-wrap">
                <div>
                  <h1 class="text-h4 white--text mb-1">{{ produto.nome || 'Detalhes do Produto' }}</h1>
                  <p class="text-subtitle-1 white--text mb-0">
                    {{ produto.tipo_produto === 'cliente' ? 'Produto do Cliente' : 'Produto do Concorrente' }}
                    <v-chip
                      v-if="produto.produto_cliente"
                      small
                      color="amber"
                      text-color="black"
                      class="ml-2"
                    >
                      <v-icon left small>mdi-star</v-icon>
                      Produto Base
                    </v-chip>
                  </p>
                </div>
                <v-spacer></v-spacer>
                <div>
                  <v-btn 
                    color="white" 
                    class="primary--text"
                    :loading="verificando"
                    @click="verificarPreco"
                  >
                    <v-icon left>mdi-refresh</v-icon>
                    Verificar Preço
                  </v-btn>
                  <v-btn 
                    v-if="produto.url"
                    text
                    color="white"
                    class="ml-2"
                    :href="produto.url" 
                    target="_blank"
                  >
                    <v-icon left>mdi-open-in-new</v-icon>
                    Abrir Site
                  </v-btn>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      
      <v-row>
        <!-- Coluna de informações do produto -->
        <v-col cols="12" md="6">
          <v-card elevation="2" class="mb-4 detail-card">
            <v-card-title class="primary--text">
              <v-icon left color="primary">mdi-information-outline</v-icon>
              Informações do Produto
            </v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item two-line>
                  <v-list-item-avatar color="primary" class="rounded white--text">
                    <v-icon>mdi-tag</v-icon>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="text-subtitle-2 text-gray">Nome</v-list-item-title>
                    <v-list-item-subtitle class="text-h6">{{ produto.nome || 'N/A' }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item two-line>
                  <v-list-item-avatar color="info" class="rounded white--text">
                    <v-icon>mdi-store</v-icon>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="text-subtitle-2 text-gray">
                      {{ produto.tipo_produto === 'cliente' ? 'Tipo' : 'Concorrente' }}
                    </v-list-item-title>
                    <v-list-item-subtitle class="text-h6">
                      {{ produto.tipo_produto === 'cliente' ? 'Produto do Cliente' : produto.concorrente || 'N/A' }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item two-line>
                  <v-list-item-avatar color="warning" class="rounded white--text">
                    <v-icon>mdi-link-variant</v-icon>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="text-subtitle-2 text-gray">URL</v-list-item-title>
                    <v-list-item-subtitle style="word-break: break-all;">
                      <a :href="produto.url" target="_blank" rel="noopener noreferrer" v-if="produto.url" class="text-decoration-none">
                        {{ produto.url }}
                      </a>
                      <span v-else>N/A</span>
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item two-line>
                  <v-list-item-avatar color="success" class="rounded white--text">
                    <v-icon>mdi-web</v-icon>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="text-subtitle-2 text-gray">Plataforma</v-list-item-title>
                    <v-list-item-subtitle>{{ produto.plataforma?.nome || 'N/A' }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item two-line>
                  <v-list-item-avatar color="error" class="rounded white--text">
                    <v-icon>mdi-clock-outline</v-icon>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="text-subtitle-2 text-gray">Última Verificação</v-list-item-title>
                    <v-list-item-subtitle>{{ formatDate(produto.ultima_verificacao) }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                
                <!-- Configuração de produto cliente base -->
                <v-list-item>
                  <v-list-item-avatar color="amber" class="rounded white--text">
                    <v-icon>mdi-star</v-icon>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="text-subtitle-2 text-gray">Produto Cliente Base</v-list-item-title>
                    <div class="mt-2">
                      <v-switch
                        v-model="produto.produto_cliente"
                        @change="atualizarProdutoClienteStatus"
                        :disabled="atualizandoStatus"
                        color="primary"
                        hide-details
                        dense
                      ></v-switch>
                      <div class="caption mt-1 text-grey">
                        Este produto será usado como base para comparações de preço
                      </div>
                    </div>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="12" md="6">
          <!-- Preço do Cliente (apenas para produtos do cliente) -->
          <v-card v-if="produto.tipo_produto === 'cliente'" elevation="2" class="mb-4 detail-card">
            <v-card-title class="primary--text">
              <v-icon left color="primary">mdi-currency-usd</v-icon>
              Preço do Cliente
            </v-card-title>
            <v-card-text>
              <v-form ref="form" v-model="formValid" class="py-3">
                <v-text-field
                  v-model="precoCliente"
                  label="Preço do Cliente"
                  prefix="R$"
                  type="number"
                  step="0.01"
                  :rules="precoRules"
                  filled
                  rounded
                  hide-details="auto"
                ></v-text-field>
                <div class="caption text-grey mt-2">
                  Este é o preço do seu produto. Atualize-o sempre que houver mudanças no valor.
                </div>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                :disabled="!formValid"
                :loading="atualizandoPreco"
                @click="atualizarPrecoCliente"
                elevation="2"
                class="px-6"
              >
                <v-icon left>mdi-content-save</v-icon>
                Atualizar Preço
              </v-btn>
            </v-card-actions>
          </v-card>
          
          <!-- Novo campo para exibir preço mais recente (para produtos concorrentes marcados como base) -->
          <v-card v-if="produto.tipo_produto === 'concorrente' && produto.produto_cliente" elevation="2" class="mb-4 warning-card">
            <v-card-title class="warning--text">
              <v-icon left color="warning">mdi-alert-circle</v-icon>
              Atenção: Configuração Inconsistente
            </v-card-title>
            <v-card-text>
              <v-alert type="warning" class="mb-4" dense>
                Este produto está marcado como produto cliente base, mas é do tipo concorrente. 
                O ideal é que o produto cliente base seja do tipo "cliente" para funcionamento correto do sistema.
              </v-alert>
              
              <v-sheet class="pa-4 rounded text-center" color="grey lighten-4">
                <div class="text-subtitle-1 mb-2">Preço Mais Recente:</div>
                <div class="text-h4 font-weight-bold primary--text">
                  {{ produto.preco_exibicao ? formatarPreco(produto.preco_exibicao) : formatarPreco(produto.menor_preco_concorrente) }}
                </div>
              </v-sheet>
              
              <div class="caption text-grey mt-3">
                Este é o preço mais recente registrado para este produto. Considere alterar o tipo para "cliente" 
                para melhor organização do sistema.
              </div>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                @click="corrigirTipoProduto"
                :loading="corrigindoTipo"
              >
                <v-icon left>mdi-check</v-icon>
                Corrigir Tipo para Cliente
              </v-btn>
            </v-card-actions>
          </v-card>
          
          <!-- Comparação de Preços (apenas para produtos do cliente) -->
          <v-card v-if="produto.tipo_produto === 'cliente'" elevation="2" class="mb-4 detail-card">
            <v-card-title class="primary--text">
              <v-icon left color="primary">mdi-compare</v-icon>
              Comparação de Preços
            </v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="text-subtitle-2 text-gray">Preço do Cliente</v-list-item-title>
                    <v-list-item-subtitle class="text-h5 font-weight-medium primary--text mt-1">
                      {{ formatarPreco(produto.preco_cliente) }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                
                <v-divider></v-divider>
                
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="text-subtitle-2 text-gray">Menor Preço Concorrente</v-list-item-title>
                    <v-list-item-subtitle class="text-h5 font-weight-medium mt-1">
                      {{ formatarPreco(produto.menor_preco_concorrente) }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                
                <v-divider v-if="produto.diferenca_percentual !== null"></v-divider>
                
                <v-list-item v-if="produto.diferenca_percentual !== null">
                  <v-list-item-content>
                    <v-list-item-title class="text-subtitle-2 text-gray">Diferença Percentual</v-list-item-title>
                    <v-list-item-subtitle class="mt-1">
                      <v-chip
                        :color="produto.diferenca_percentual <= 0 ? 'success' : 'error'"
                        class="font-weight-bold text-h6 px-4 py-2"
                        :text-color="produto.diferenca_percentual <= 0 ? 'white' : 'white'"
                        large
                      >
                        {{ formatarPercentual(produto.diferenca_percentual) }}
                      </v-chip>
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
              
              <!-- Status visual de comparação -->
              <v-sheet 
                v-if="produto.diferenca_percentual !== null" 
                color="grey lighten-4" 
                class="pa-4 rounded mt-4"
              >
                <div class="text-center">
                  <v-icon 
                    :color="produto.diferenca_percentual <= 0 ? 'success' : 'error'"
                    size="64"
                  >
                    {{ produto.diferenca_percentual <= 0 ? 'mdi-thumb-up' : 'mdi-thumb-down' }}
                  </v-icon>
                  <div class="text-subtitle-1 mt-2">
                    {{ produto.diferenca_percentual <= 0 ? 'Seu preço está competitivo!' : 'Seu preço está acima da concorrência' }}
                  </div>
                </div>
              </v-sheet>
            </v-card-text>
          </v-card>
          
          <!-- Alerta se não houver concorrentes -->
          <v-alert
            v-if="produto.tipo_produto === 'cliente' && produto.menor_preco_concorrente === null"
            type="info"
            class="mb-4"
            outlined
            icon="mdi-alert-circle-outline"
          >
            <div class="text-subtitle-1 font-weight-medium mb-2">Sem Concorrentes Registrados</div>
            <p class="mb-0">Não há preços de concorrentes registrados para esse produto. Cadastre produtos concorrentes com o mesmo nome para habilitar a comparação.</p>
            <div class="mt-4">
              <v-btn
                color="primary"
                small
                outlined
                @click="$router.push('/products/add')"
              >
                <v-icon left small>mdi-plus</v-icon>
                Adicionar Concorrente
              </v-btn>
            </div>
          </v-alert>
        </v-col>
      </v-row>
    </template>
    
    <!-- Snackbar para mensagens de sucesso/erro -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
      right
      bottom
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
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const verificando = ref(false)
const atualizandoPreco = ref(false)
const atualizandoStatus = ref(false)
const corrigindoTipo = ref(false)
const produto = ref({})
const precoCliente = ref(0)
const formValid = ref(false)
const form = ref(null)

// Snackbar state
const snackbar = ref({
  show: false,
  text: '',
  color: 'success',
  timeout: 3000
})

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

// Exibir mensagem no snackbar
const mostrarSnackbar = (texto, cor = 'success', timeout = 3000) => {
  snackbar.value = {
    show: true,
    text: texto,
    color: cor,
    timeout: timeout
  }
}

// Função para corrigir o tipo do produto
const corrigirTipoProduto = async () => {
  corrigindoTipo.value = true;
  try {
    await api.patch(`/produtos/${produto.value.id}/`, {
      tipo_produto: 'cliente'
    });
    
    produto.value.tipo_produto = 'cliente';
    mostrarSnackbar('Tipo do produto corrigido para Cliente', 'success');
    
    // Recarregar o produto para atualizar as interfaces
    await carregarProduto();
  } catch (error) {
    console.error('Erro ao corrigir tipo do produto:', error);
    mostrarSnackbar('Erro ao corrigir tipo do produto', 'error');
  } finally {
    corrigindoTipo.value = false;
  }
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
    
    // Inconsistência detectada: produto marcado como produto_cliente mas tipo é concorrente
    if (produto.value.produto_cliente && produto.value.tipo_produto === 'concorrente') {
      console.warn('Inconsistência: Produto marcado como produto_cliente, mas é do tipo concorrente:', produto.value);
      // Podemos mostrar um aviso para o usuário
      mostrarSnackbar('Este produto está marcado como produto cliente base, mas é do tipo concorrente. Considere ajustar o tipo.', 'warning', 6000);
    }
    
    // Atualiza o campo de preço para produtos do tipo cliente
    if (produto.value.tipo_produto === 'cliente') {
      // Se o preço do cliente estiver definido no produto, use-o
      if (produto.value.preco_cliente !== null && produto.value.preco_cliente !== undefined) {
        precoCliente.value = produto.value.preco_cliente;
      } else {
        // Se o preço do cliente não estiver definido, inicializa com zero
        precoCliente.value = 0;
        // E atualiza o objeto do produto para evitar "null" na exibição
        produto.value.preco_cliente = 0;
      }
    }
    
    // Carregar o histórico de preços
    try {
      const historicoResponse = await api.get(`/produtos/${produtoId}/historico/`);
      if (historicoResponse.data && historicoResponse.data.length > 0) {
        // Usar o preço mais recente do histórico, se disponível
        const precoMaisRecente = parseFloat(historicoResponse.data[0].preco);
        console.log('Preço mais recente do histórico:', precoMaisRecente);
        
        // Para produtos do cliente, atualizar o preço se não estiver definido
        if (produto.value.tipo_produto === 'cliente' && 
            (produto.value.preco_cliente === null || produto.value.preco_cliente === undefined || produto.value.preco_cliente === 0)) {
          produto.value.preco_cliente = precoMaisRecente;
          precoCliente.value = precoMaisRecente;
        }
        
        // Para produtos do tipo concorrente marcados como produto_cliente (inconsistente),
        // precisamos exibir o preço mais recente em algum lugar
        if (produto.value.tipo_produto === 'concorrente' && produto.value.produto_cliente) {
          // Como é concorrente, não podemos usar preco_cliente, então vamos armazenar em uma propriedade auxiliar
          produto.value.preco_exibicao = precoMaisRecente;
        }
      }
    } catch (error) {
      console.error('Erro ao carregar histórico de preços:', error);
      // Continuar mesmo se o histórico falhar, não é crítico
    }
    
  } catch (error) {
    console.error('Erro ao carregar produto:', error);
    produto.value = {};
    mostrarSnackbar('Erro ao carregar produto', 'error');
  } finally {
    loading.value = false;
  }
}

// Atualizar status de produto cliente
const atualizarProdutoClienteStatus = async () => {
  atualizandoStatus.value = true;
  try {
    // Verificar se o usuário tem um cliente atual definido
    const userInfo = await api.get('/user/info/');
    if (!userInfo.data.cliente_atual) {
      mostrarSnackbar('Por favor, selecione um cliente atual antes de continuar', 'warning');
      return;
    }

    // Obter o ID do cliente atual (pode ser objeto ou ID direto)
    const clienteId = typeof userInfo.data.cliente_atual === 'object' 
      ? userInfo.data.cliente_atual.id 
      : userInfo.data.cliente_atual;
    
    // Obter o ID do grupo (pode ser objeto ou ID direto)
    const grupoId = typeof produto.value.grupo === 'object' 
      ? produto.value.grupo.id 
      : produto.value.grupo;
    
    // Sempre incluir cliente e grupo no payload do PATCH para evitar erro
    const dadosAtualizacao = {
      produto_cliente: produto.value.produto_cliente,
      cliente: clienteId,
      grupo: grupoId
    };
    
    // Se estiver ativando a opção produto_cliente
    if (produto.value.produto_cliente) {
      // Se o tipo atual for concorrente, alterá-lo para cliente
      if (produto.value.tipo_produto === 'concorrente') {
        dadosAtualizacao.tipo_produto = 'cliente';
        // Atualizar também localmente
        produto.value.tipo_produto = 'cliente';
        console.log('Alterando o tipo do produto de concorrente para cliente:', dadosAtualizacao);
      }
      
      // Desmarcar outros produtos com o mesmo nome que possam estar marcados como base
      try {
        // Obter todos os produtos com o mesmo nome
        const produtosResponse = await api.get(`/produtos/?nome=${produto.value.nome}`);
        const produtosDoMesmoNome = produtosResponse.data.results || [];
        
        // Filtrar apenas os que estão marcados como produto_cliente e não são o atual
        const produtosClienteBase = produtosDoMesmoNome.filter(p => 
          p.id !== produto.value.id && 
          p.produto_cliente === true && 
          p.nome === produto.value.nome
        );
        
        // Desmarcar cada um deles
        for (const produtoAnterior of produtosClienteBase) {
          console.log(`Desmarcando produto ${produtoAnterior.id} como cliente base`);
          await api.patch(`/produtos/${produtoAnterior.id}/`, {
            produto_cliente: false,
            cliente: clienteId,
            grupo: grupoId
          });
        }
      } catch (err) {
        console.error('Erro ao verificar outros produtos marcados como base:', err);
        // Continuar mesmo se houver falha aqui
      }
    }
    
    console.log('Enviando dados de atualização:', dadosAtualizacao);
    
    // Atualizar o produto com o novo status e tipo (se aplicável)
    await api.patch(`/produtos/${produto.value.id}/`, dadosAtualizacao);
    
    // Mensagem personalizada com base na ação realizada
    if (produto.value.produto_cliente) {
      mostrarSnackbar('Produto definido como produto cliente base', 'success');
      
      // Se mudamos o tipo, recarregar o produto para atualizar a interface
      if (dadosAtualizacao.tipo_produto) {
        await carregarProduto();
      }
    } else {
      mostrarSnackbar('Produto removido como produto cliente base', 'success');
    }
    
  } catch (error) {
    console.error('Erro ao atualizar status de produto cliente:', error);
    // Reverter a mudança no modelo local em caso de erro
    produto.value.produto_cliente = !produto.value.produto_cliente;
    
    // Se houve mudança de tipo, também reverter isso
    if (produto.value.tipo_produto === 'cliente' && !produto.value.produto_cliente) {
      produto.value.tipo_produto = 'concorrente';
    }
    
    mostrarSnackbar('Erro ao atualizar status de produto cliente: ' + 
      (error.response?.data?.detail || error.message), 'error');
  } finally {
    atualizandoStatus.value = false;
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
    
    mostrarSnackbar('Preço verificado com sucesso');
    
  } catch (error) {
    console.error('Erro ao verificar preço:', error);
    mostrarSnackbar('Erro ao verificar preço', 'error');
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
    
    mostrarSnackbar('Preço atualizado com sucesso');
    
  } catch (error) {
    console.error('Erro ao atualizar preço do cliente:', error);
    mostrarSnackbar('Erro ao atualizar preço do cliente', 'error');
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
.gradient-header {
  background: linear-gradient(135deg, var(--v-primary-base) 0%, var(--v-primary-darken1) 100%);
  border-radius: 8px;
  color: white;
}

.detail-card {
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.detail-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
}

.warning-card {
  border-left: 4px solid var(--v-warning-base);
  border-radius: 8px;
  overflow: hidden;
}

.text-gray {
  color: rgba(0, 0, 0, 0.6);
}

.rounded {
  border-radius: 50%;
}

:deep(.v-list-item__avatar) {
  margin-right: 16px !important;
}

:deep(.v-list-item) {
  padding: 16px !important;
}

.transition-swing {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
}

.transition-swing:hover {
  transform: translateX(-4px);
}
</style>