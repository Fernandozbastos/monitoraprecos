<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
      v-if="isAuthenticated"
    >
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>MonitoraPreços</v-toolbar-title>
        <!-- Adicionar o seletor de cliente aqui -->
      <v-select
        v-model="clienteAtual"
        :items="clientesDisponiveis"
        item-title="nome"
        item-value="id"
        label="Cliente atual"
        hide-details
        dense
        class="ml-4 mt-3"
        style="max-width: 200px; color: white;"
        :loading="carregandoClientes"
        @change="atualizarClienteAtual"
      >
        <template v-slot:selection="{ item }">
          <span class="white--text">{{ item.raw.nome }}</span>
        </template>
      </v-select>

      <v-spacer></v-spacer>
      <v-btn icon @click="logout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      app
      temporary
      v-if="isAuthenticated"
    >
      <v-list-item>
        <template v-slot:prepend>
          <v-avatar>
            <v-icon>mdi-account-circle</v-icon>
          </v-avatar>
        </template>
        <v-list-item-title>{{ userName }}</v-list-item-title>
        <v-list-item-subtitle>{{ userType }}</v-list-item-subtitle>
      </v-list-item>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :to="item.path"
          link
        >
          <template v-slot:prepend>
            <v-icon>{{ item.icon }}</v-icon>
          </template>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
        <v-divider class="my-2"></v-divider>
  
        <v-list-item
          to="/products/add"
          link
        >
          <template v-slot:prepend>
            <v-icon color="success">mdi-plus-circle</v-icon>
          </template>
          <v-list-item-title>Adicionar Produto</v-list-item-title>
        </v-list-item>
      </v-list>
      
    </v-navigation-drawer>

    <v-main>
      <router-view />
        <!-- Botão flutuante para adicionar produtos -->
        <v-btn
        v-if="isAuthenticated && showFab"
        fab
        large
        color="success"
        fixed
        bottom
        right
        class="mb-4 mr-4"
        @click="$router.push('/products/add')"
        >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-main>

    <v-footer app>
      <span>&copy; {{ new Date().getFullYear() }} MonitoraPreços</span>
    </v-footer>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import api from '@/services/api'


const store = useStore()
const router = useRouter()
const drawer = ref(false)
const clienteAtual = ref(null)
const clientesDisponiveis = ref([])
const carregandoClientes = ref(false)

const menuItems = [
  { title: 'Dashboard', path: '/dashboard', icon: 'mdi-view-dashboard' },
  { title: 'Produtos', path: '/products', icon: 'mdi-package-variant-closed' },
  { title: 'Meu Perfil', path: '/profile', icon: 'mdi-account-cog' },
]

// Computed properties
const isAuthenticated = computed(() => store.getters['auth/isAuthenticated'])
const user = computed(() => store.getters['auth/user'])
const userName = computed(() => user.value ? user.value.username : '')
const userType = computed(() => 
  user.value ? (user.value.tipo === 'admin' ? 'Administrador' : 'Usuário') : ''
)

// Computed property para controlar quando mostrar o FAB
const showFab = computed(() => {
  // Mostrar apenas nas páginas de listagem e dashboard
  const route = router.currentRoute.value
  return route.path === '/products' || route.path === '/dashboard'
})

// Função para carregar os clientes disponíveis
const carregarClientes = async () => {
  if (!isAuthenticated.value) return
  
  carregandoClientes.value = true
  try {
    const response = await api.get('/clientes/')
    clientesDisponiveis.value = response.data.results || []
    
    // Define o cliente atual se o usuário já tiver um
    if (user.value && user.value.cliente_atual) {
      clienteAtual.value = user.value.cliente_atual
    } else if (clientesDisponiveis.value.length > 0) {
      // Se não tiver um cliente atual, define o primeiro da lista
      clienteAtual.value = clientesDisponiveis.value[0].id
      // E atualiza o cliente atual no backend
      await atualizarClienteAtual()
    }
  } catch (error) {
    console.error('Erro ao carregar clientes:', error)
  } finally {
    carregandoClientes.value = false
  }
}

// Função para atualizar o cliente atual do usuário
const atualizarClienteAtual = async () => {
  if (!clienteAtual.value) return
  
  try {
    await api.post('/user/set-cliente/', { cliente_atual: clienteAtual.value })
    
    // Atualiza o usuário no Vuex store
    const userInfo = await api.get('/user/info/')
    store.commit('auth/setUser', userInfo.data)
    
    // Recarrega a página atual para atualizar os dados
    router.go(0)
  } catch (error) {
    console.error('Erro ao atualizar cliente atual:', error)
  }
}

// Carregar clientes quando o componente for montado
onMounted(() => {
  if (isAuthenticated.value) {
    carregarClientes()
  }
})

// Observar mudanças na autenticação
watch(() => isAuthenticated.value, (newValue) => {
  if (newValue) {
    carregarClientes()
  }
})

// Métodos
const logout = () => {
  store.dispatch('auth/logout')
}
</script>