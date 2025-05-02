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
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>

    <v-footer app>
      <span>&copy; {{ new Date().getFullYear() }} MonitoraPreços</span>
    </v-footer>
  </v-app>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()
const drawer = ref(false)

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

// Métodos
const logout = () => {
  store.dispatch('auth/logout')
}
</script>