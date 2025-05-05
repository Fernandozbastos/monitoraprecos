// Formatação de preço
export const formatarPreco = (valor) => {
    if (valor === null || valor === undefined || isNaN(valor)) {
      return 'N/A';
    }
    
    // Garantir que seja tratado como número
    const numero = Number(valor);
    if (isNaN(numero)) {
      return 'N/A';
    }
    
    return `R$ ${numero.toFixed(2).replace('.', ',')}`;
  }
  
  // Formatação de percentual
  export const formatarPercentual = (valor) => {
    if (valor === null || valor === undefined || isNaN(valor)) {
      return 'N/A';
    }
    
    // Garantir que seja tratado como número
    const numero = Number(valor);
    if (isNaN(numero)) {
      return 'N/A';
    }
    
    const sinal = numero > 0 ? '+' : '';
    return `${sinal}${numero.toFixed(1).replace('.', ',')}%`;
  }
  
  // Determinar a cor da diferença
  export const getCorDiferenca = (diferenca) => {
    if (diferenca === null || diferenca === undefined || isNaN(diferenca)) return 'grey';
    return diferenca <= 0 ? 'success' : 'error';
  }
  
  // Formatar data
  export const formatDate = (dateString) => {
    if (!dateString) return 'Nunca verificado';
    try {
      const options = { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleString('pt-BR', options);
    } catch (error) {
      console.error('Erro ao formatar data:', error);
      return dateString || '-';
    }
  }
  
  // Formatação de data mais simples para o gráfico
  export const formatDateShort = (dateString) => {
    if (!dateString) return '';
    const options = { day: '2-digit', month: '2-digit', year: '2-digit' };
    try {
      return new Date(dateString).toLocaleString('pt-BR', options);
    } catch (e) {
      console.error('Erro ao formatar data curta:', e);
      return dateString;
    }
  }