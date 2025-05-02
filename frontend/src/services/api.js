// src/services/api.js
import axios from 'axios'
import store from '../store' // Importar o store diretamente

// Cria uma instância do axios com URL base
const apiClient = axios.create({
  baseURL: '/api',  // Isso usará o proxy configurado no Vite
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000
})

// Adiciona console.log para depuração de requisições
apiClient.interceptors.request.use(
  config => {
    // Usar store diretamente
    const token = store.getters['auth/accessToken']
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    
    // Log de depuração para PATCH requests
    if (config.method === 'patch') {
      console.log('PATCH request data:', config.data);
    }
    
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Intercepta as respostas para logar as respostas do patch
apiClient.interceptors.response.use(
  response => {
    // Log de depuração para respostas de PATCH requests
    if (response.config.method === 'patch') {
      console.log('PATCH response data:', response.data);
    }
    return response
  },
  async error => {
    // Usar store diretamente
    const originalRequest = error.config
    
    // Se recebeu 401 (não autorizado) e não for uma tentativa de refresh
    if (error.response && error.response.status === 401 && !originalRequest._retry && 
        originalRequest.url !== '/token/refresh/') {
      originalRequest._retry = true
      
      try {
        // Tenta renovar o token
        const refreshToken = store.getters['auth/refreshToken']
        if (!refreshToken) {
          // Se não tiver refresh token, desloga
          store.dispatch('auth/logout')
          return Promise.reject(error)
        }
        
        const response = await axios.post(
          '/api/token/refresh/',
          { refresh: refreshToken }
        )
        
        const { access } = response.data
        await store.dispatch('auth/refreshToken', { access })
        
        // Refaz a requisição original com o novo token
        originalRequest.headers['Authorization'] = `Bearer ${access}`
        return apiClient(originalRequest)
      } catch (err) {
        // Se falhar, desloga
        store.dispatch('auth/logout')
        return Promise.reject(error)
      }
    }
    
    // Log detalhado de erros para PATCH requests
    if (error.config && error.config.method === 'patch') {
      console.error('PATCH request error:', {
        url: error.config.url,
        data: error.config.data,
        response: error.response?.data
      });
    }
    
    return Promise.reject(error)
  }
)

export default apiClient