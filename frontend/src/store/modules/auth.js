// src/store/modules/auth.js
import authService from '@/services/auth_services'
import { jwtDecode } from 'jwt-decode'
import router from '@/router'

const state = {
  accessToken: localStorage.getItem('accessToken') || null,
  refreshToken: localStorage.getItem('refreshToken') || null,
  user: JSON.parse(localStorage.getItem('user')) || null,
  loading: false,
  error: null
}

const getters = {
  isAuthenticated: state => !!state.accessToken,
  accessToken: state => state.accessToken,
  refreshToken: state => state.refreshToken,
  user: state => state.user,
  loading: state => state.loading,
  error: state => state.error
}

const actions = {
  async login({ commit }, credentials) {
    commit('setLoading', true)
    commit('clearError')
    
    try {
      const response = await authService.login(credentials)
      const { access, refresh } = response.data
      
      // Decodifica o token para obter informações básicas
      const decoded = jwtDecode(access)
      
      commit('setAuth', { access, refresh, decoded })
      
      // Busca informações detalhadas do usuário
      const userInfo = await authService.getUserInfo()
      commit('setUser', userInfo.data)
      
      router.push('/dashboard')
      return userInfo.data
    } catch (error) {
      commit('setError', error.response?.data?.detail || 'Erro ao fazer login')
      throw error
    } finally {
      commit('setLoading', false)
    }
  },
  
  async refreshToken({ commit, state }) {
    try {
      const response = await authService.refreshToken(state.refreshToken)
      const { access } = response.data
      const decoded = jwtDecode(access)
      
      commit('updateAccessToken', { access, decoded })
      return access
    } catch (error) {
      commit('clearAuth')
      router.push('/login')
      throw error
    }
  },
  
  logout({ commit }) {
    commit('clearAuth')
    router.push('/login')
  },
  
  // Nova action para verificar a validade do token
  checkAuth({ state, dispatch }) {
    if (!state.accessToken) return false
    
    try {
      const decoded = jwtDecode(state.accessToken)
      const currentTime = Date.now() / 1000
      
      // Se o token expirou, tenta renovar
      if (decoded.exp < currentTime) {
        return dispatch('refreshToken')
      }
      
      return true
    } catch (error) {
      return false
    }
  },
  
  // Ação para atualizar dados do usuário
  async updateUserInfo({ commit }) {
    try {
      const userInfo = await authService.getUserInfo()
      commit('setUser', userInfo.data)
      return userInfo.data
    } catch (error) {
      console.error('Erro ao atualizar dados do usuário:', error)
      throw error
    }
  }
}

const mutations = {
  setLoading(state, loading) {
    state.loading = loading
  },
  
  setError(state, error) {
    state.error = error
  },
  
  clearError(state) {
    state.error = null
  },
  
  setAuth(state, { access, refresh, decoded }) {
    state.accessToken = access
    state.refreshToken = refresh
    
    localStorage.setItem('accessToken', access)
    localStorage.setItem('refreshToken', refresh)
  },
  
  updateAccessToken(state, { access, decoded }) {
    state.accessToken = access
    localStorage.setItem('accessToken', access)
  },
  
  setUser(state, user) {
    // Garantir que cliente_atual seja sempre o ID
    if (user.cliente_atual && typeof user.cliente_atual === 'object') {
      user.cliente_atual = user.cliente_atual.id
    }
    
    state.user = user
    localStorage.setItem('user', JSON.stringify(user))
  },
  
  clearAuth(state) {
    state.accessToken = null
    state.refreshToken = null
    state.user = null
    
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}