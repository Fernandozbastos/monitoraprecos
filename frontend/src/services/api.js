// src/services/api.js
import axios from 'axios'
import store from '../store'
import router from '../router'

// Cria uma instância do axios com URL base
const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000
})

// Interceptor de request
apiClient.interceptors.request.use(
  config => {
    const token = store.getters['auth/accessToken']
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Interceptor de response
apiClient.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config
    
    // Se recebeu 401 (não autorizado)
    if (error.response.status === 401) {
      // Se não for uma tentativa de refresh token e não for o login
      if (!originalRequest._retry && !originalRequest.url.includes('/token/')) {
        originalRequest._retry = true
        
        try {
          const refreshToken = store.getters['auth/refreshToken']
          
          if (!refreshToken) {
            throw new Error('No refresh token available')
          }
          
          // Usar uma instância separada para evitar interceptors
          const response = await axios.post('/api/token/refresh/', {
            refresh: refreshToken
          })
          
          const { access } = response.data
          
          // Atualizar o token
          store.commit('auth/setAuth', { 
            access, 
            refresh: refreshToken
          })
          
          // Atualizar o header da requisição original
          originalRequest.headers['Authorization'] = `Bearer ${access}`
          
          // Refazer a requisição original
          return apiClient(originalRequest)
        } catch (err) {
          // Se falhar, desloga
          store.dispatch('auth/logout')
          router.push('/login')
          return Promise.reject(error)
        }
      } else {
        // Se for uma tentativa de refresh token que falhou, desloga
        store.dispatch('auth/logout')
        router.push('/login')
      }
    }
    
    return Promise.reject(error)
  }
)

export default apiClient