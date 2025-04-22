// src/store/index.js
import { createStore } from 'vuex'
import auth from './modules/auth'
import VuexPersistence from 'vuex-persist'

// Configura persistência para o Vuex (salva estado no localStorage)
const vuexLocal = new VuexPersistence({
  key: 'monitoraprecos',
  storage: window.localStorage,
  modules: ['auth']
})

export default createStore({
  modules: {
    auth
  },
  plugins: [vuexLocal.plugin]
})