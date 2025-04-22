// src/services/auth.service.js
import api from './api'
import axios from 'axios'

// URL base da API (sem o /api para autenticação)
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const authService = {
  login(credentials) {
    return axios.post(`${BASE_URL}/api/token/`, credentials)
  },
  
  refreshToken(refreshToken) {
    return axios.post(`${BASE_URL}/api/token/refresh/`, { refresh: refreshToken })
  },
  
  verifyToken(token) {
    return axios.post(`${BASE_URL}/api/token/verify/`, { token })
  },
  
  getUserInfo() {
    return api.get('/user/info/')
  },
  
  changePassword(passwords) {
    return api.post('/user/change-password/', passwords)
  }
}

export default authService