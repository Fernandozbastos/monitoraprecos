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
              <v-list>
                <v-list-item>
                  <div>
                    <div class="text-caption text-gray">Nome</div>
                    <div class="text-h6">{{ produto.nome || 'N/A' }}</div>
                  </div>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item>
                  <div>
                    <div class="text-caption text-gray">Tipo</div>
                    <div>
                      {{ produto.tipo_produto === 'cliente' ? 'Produto do Cliente' : 'Produto de Concorrente' }}
                    </div>
                  </div>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item v-if="produto.tipo_produto === 'concorrente'">
                  <div>
                    <div class="text-caption text-gray">Concorrente</div>
                    <div>{{ produto.concorrente || 'N/A' }}</div>
                  </div>
                </v-list-item>
                <v-divider v-if="produto.tipo_produto === 'concorrente'"></v-divider>
                
                <v-list-item>
                  <div>
                    <div class="text-caption text-gray">URL</div>
                    <div>
                      <a :href="produto.url" target="_blank" rel="noopener noreferrer" v-if="produto.url">
                        {{ produto.url }}
                      </a>
                      <span v-else>N/A</span>
                    </div>
                  </div>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item>
                  <div>
                    <div class="text-caption text-gray">Plataforma</div>
                    <div>{{ produto.plataforma?.nome || 'N/A' }}</div>
                  </div>
                </v-list-item>
                <v-divider></v-divider>
                
                <v-list-item>
                  <div>
                    <div class="text-caption text-gray">Última Verificação</div>
                    <div>{{ formatDate(produto.ultima_verificacao) }}</div>
                  </div>
                </v-list-item>
                <v-divider></v-divider>
                
                <!-- Novo campo para marcar como produto cliente base -->
                <v-list-item>
                  <div>
                    <div class="text-caption text-gray">Produto Cliente Base</div>
                    <div>
                      <v-switch
                        v-model="produto.produto_cliente"
                        @change="atualizarProdutoClienteStatus"
                        :disabled="atualizandoStatus"
                        color="primary"
                        hide-details
                        dense
                      ></v-switch>
                    </div>
                  </div>
                </v-list-item>
              </v-list>
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
          
          <!-- Novo campo para exibir preço mais recente (para produtos concorrentes marcados como base) -->
          <v-card v-if="produto.tipo_produto === 'concorrente' && produto.produto_cliente" elevation="2" class="mb-4">
            <v-card-title>Preço Mais Recente</v-card-title>
            <v-card-text>
              <v-alert type="warning" class="mb-4">
                Este produto está marcado como produto cliente base, mas é do tipo concorrente. 
                O ideal é que o produto cliente base seja do tipo "cliente" para funcionamento correto do sistema.
              </v-alert>
              
              <div class="text-h5 font-weight-bold">
                {{ produto.preco_exibicao ? formatarPreco(produto.preco_exibicao) : formatarPreco(produto.menor_preco_concorrente) }}
              </div>
              
              <div class="mt-2 text-caption">
                Este é o preço mais recente registrado para este produto.
              </div>
            </v-card-text>
          </v-card>
          
          <!-- Comparação de Preços (apenas para produtos do cliente) -->
          <v-card v-if="produto.tipo_produto === 'cliente'" elevation="2" class="mb-4">
            <v-card-title>
              Comparação de Preços
            </v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item>
                  <div>
                    <div class="text-caption text-gray">Preço do Cliente</div>
                    <div class="text-h6">
                      {{ formatarPreco(produto.preco_cliente) }}
                    </div>
                  </div>
                </v-list-item>
                
                <v-list-item>
                  <div>
                    <div class="text-caption text-gray">Menor Preço Concorrente</div>
                    <div class="text-h6">
                      {{ formatarPreco(produto.menor_preco_concorrente) }}
                    </div>
                  </div>
                </v-list-item>
                
                <v-list-item v-if="produto.diferenca_percentual !== null">
                  <div>
                    <div class="text-caption text-gray">Diferença Percentual</div>
                    <div>
                      <v-chip
                        :color="produto.diferenca_percentual <= 0 ? 'success' : 'error'"
                        class="font-weight-bold"
                        :text-color="produto.diferenca_percentual <= 0 ? 'white' : 'white'"
                      >
                        {{ formatarPercentual(produto.diferenca_percentual) }}
                      </v-chip>
                    </div>
                  </div>
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
    
    <!-- Snackbar para mensagens de sucesso/erro -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
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
    // Se estiver marcando como produto_cliente=true e o tipo for concorrente,
    // também alterar o tipo para cliente
    const dadosAtualizacao = {
      produto_cliente: produto.value.produto_cliente
    };
    
    // Se estiver ativando a opção produto_cliente e o tipo atual for concorrente
    if (produto.value.produto_cliente && produto.value.tipo_produto === 'concorrente') {
      // Incluir a mudança de tipo no payload da atualização
      dadosAtualizacao.tipo_produto = 'cliente';
      
      // Atualizar também localmente
      produto.value.tipo_produto = 'cliente';
      
      console.log('Alterando o tipo do produto de concorrente para cliente:', dadosAtualizacao);
    }
    
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
    
    mostrarSnackbar('Erro ao atualizar status de produto cliente', 'error');
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
.v-chip {
  font-weight: bold;
}

.text-gray {
  color: rgba(0, 0, 0, 0.6);
}
</style>