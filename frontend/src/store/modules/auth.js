// src/store/modules/auth.js
import authService from '@/services/auth_services'
import { jwtDecode } from 'jwt-decode'
import router from '@/router'

const state = {
  accessToken: localStorage.getItem('accessToken') || null,
  refreshToken: localStorage.getItem('refreshToken') || null,
  user: null,
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
      
      commit('setAuth', { access, refresh })
      
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
      
      commit('updateAccessToken', { access })
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
  
  // Action para verificar autenticação ao carregar o app
  async checkAuth({ state, dispatch, commit }) {
    try {
      if (!state.accessToken) return false
      
      // Verificar se o token ainda é válido
      const decoded = jwtDecode(state.accessToken)
      const currentTime = Date.now() / 1000
      
      // Se o token expirou, tenta renovar
      if (decoded.exp < currentTime) {
        if (state.refreshToken) {
          const newToken = await dispatch('refreshToken')
          if (newToken) {
            // Carregar dados do usuário
            const userInfo = await authService.getUserInfo()
            commit('setUser', userInfo.data)
            return true
          }
        }
        return false
      }
      
      // Se o token é válido mas não temos dados do usuário, carrega
      if (!state.user) {
        try {
          const userInfo = await authService.getUserInfo()
          commit('setUser', userInfo.data)
        } catch (error) {
          console.error('Erro ao carregar dados do usuário:', error)
        }
      }
      
      return true
    } catch (error) {
      console.error('Erro ao verificar autenticação:', error)
      return false
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
  
  setAuth(state, { access, refresh }) {
    state.accessToken = access
    state.refreshToken = refresh
    
    localStorage.setItem('accessToken', access)
    localStorage.setItem('refreshToken', refresh)
  },
  
  updateAccessToken(state, { access }) {
    state.accessToken = access
    localStorage.setItem('accessToken', access)
  },
  
  setUser(state, user) {
    state.user = user
  },
  
  clearAuth(state) {
    state.accessToken = null
    state.refreshToken = null
    state.user = null
    
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}