// src/services/auth.service.js
import api from './api'
import axios from 'axios'

// URL base da API para autenticação
const BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

const authService = {
  login(credentials) {
    console.log('Attempting login to:', `${BASE_URL}/api/token/`)
    return axios.post(`${BASE_URL}/api/token/`, credentials)
  },
  
  refreshToken(refreshToken) {
    console.log('Refreshing token')
    return axios.post(`${BASE_URL}/api/token/refresh/`, { refresh: refreshToken })
  },
  
  verifyToken(token) {
    return axios.post(`${BASE_URL}/api/token/verify/`, { token })
  },
  
  getUserInfo() {
    console.log('Getting user info')
    return api.get('user/info/')  // No leading slash, api.js will add it
  },
  
  changePassword(passwords) {
    return api.post('user/change-password/', passwords)
  },
  
  setClienteAtual(clienteId) {
    return api.post('user/set-cliente/', { cliente_atual: clienteId })
  }
}

export default authService