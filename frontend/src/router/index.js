// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

// Importações de componentes
import Login from '../views/Login.vue'

// Lazy loading para componentes
const Dashboard = () => import('../views/Dashboard.vue')
const ProductList = () => import('../views/ProductList.vue')
const ProductDetail = () => import('../views/ProductDetail.vue')
const UserProfile = () => import('../views/UserProfile.vue')
const ProductForm = () => import('../views/ProductForm.vue')


const routes = [
  {
    path: '/products/add',
    name: 'ProductAdd',
    component: ProductForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/products/:id/edit',
    name: 'ProductEdit',
    component: ProductForm,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/products',
    name: 'Products',
    component: ProductList,
    meta: { requiresAuth: true }
  },
  {
    path: '/products/:id',
    name: 'ProductDetail',
    component: ProductDetail,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'UserProfile',
    component: UserProfile,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guarda de navegação para proteger rotas
router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  
  // Verificar autenticação
  const isAuthenticated = await store.dispatch('auth/checkAuth')
  
  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router