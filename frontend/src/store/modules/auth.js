// src/store/modules/auth.js
import authService from '@/services/auth.service'
import jwtDecode from 'jwt-decode'
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
  
  async refreshToken({ commit, state }, payload) {
    if (payload && payload.access) {
      const decoded = jwtDecode(payload.access)
      commit('updateAccessToken', { access: payload.access, decoded })
      return payload.access
    }
    
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