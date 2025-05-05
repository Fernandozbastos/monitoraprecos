<!-- frontend/src/components/test/ChartTest.vue -->
<template>
    <div>
      <h2>Teste Simple de Chart.js</h2>
      <div style="width: 100%; height: 400px; border: 1px solid red;">
        <canvas ref="testChart"></canvas>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import Chart from 'chart.js/auto'
  
  const testChart = ref(null)
  
  onMounted(() => {
    try {
      const ctx = testChart.value.getContext('2d')
      
      // Dados de teste simples
      const data = {
        labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril'],
        datasets: [{
          label: 'Vendas',
          data: [12, 19, 3, 5],
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }]
      }
      
      // Criar o gráfico
      new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      })
      
      console.log('Gráfico de teste criado com sucesso!')
    } catch (error) {
      console.error('Erro ao criar gráfico de teste:', error)
    }
  })
  </script>