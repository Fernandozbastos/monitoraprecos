import { ref } from 'vue'

export const useSnackbar = () => {
  const snackbar = ref({
    show: false,
    text: '',
    color: 'success',
    timeout: 3000
  })

  const mostrarSnackbar = (texto, cor = 'success', timeout = 3000) => {
    snackbar.value = {
      show: true,
      text: texto,
      color: cor,
      timeout: timeout
    }
  }

  const fecharSnackbar = () => {
    snackbar.value.show = false
  }

  return {
    snackbar,
    mostrarSnackbar,
    fecharSnackbar
  }
}