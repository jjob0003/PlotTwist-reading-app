<template>
  <!-- Page container with padding and styling -->
  <div class="px-4 py-8 bg-white rounded-xl shadow-md relative min-h-screen">

    <!-- Back button in top-left -->
    <button
      @click="goBack"
      class="absolute top-4 left-4 text-sm bg-purple-100 text-purple-700 px-4 py-1 rounded hover:bg-purple-200 transition"
    >
      ← Back
    </button>

    <!-- Title -->
    <h2 class="text-2xl font-bold mb-6 text-center text-purple-700">
      📊 Reading Participation by Generation
    </h2>

    <!-- Content layout: text and chart side by side on large screens -->
    <div class="flex flex-col md:flex-row gap-6 mb-8">
     
      <!-- Left: Narrative explanation -->
      <div class="md:w-1/2 text-gray-800 text-base leading-relaxed">
        <p class="mb-4">
          📉 <strong>Sooo… turns out your grandma reads more than you.</strong> No shade — but see those pink and blue bars climbing up with each generation? That’s not just data. That’s a <strong>plot twist</strong>.
        </p>
        <p class="mb-4">
          🧠 Gen Z reads the least, even though we’ve got the most screens, stories, and spicy BookTok recs.
        </p>
        <p class="mb-4">
          😓 Why? Because most reading tools still feel like 2005 worksheets with Wi-Fi.
        </p>
        <p class="mb-4">
          🚀 We made <strong>PlotTwist</strong> to change that — no logins, no grades, just creative chaos: games, debates, visual lists, and moodboards.
        </p>
        <p>
          👉 <strong>Reading, but rebranded. Ready to flip the trend?</strong>
        </p>
      </div>

      <!-- Right: Chart container (Plotly will render inside this) -->
      <div ref="chart" class="md:w-1/2" style="height: 500px;"></div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import Plotly from 'plotly.js-dist-min'

const chart = ref(null)
const router = useRouter()

const goBack = () => {
  router.back()
}

onMounted(async () => {
  try {
    const res = await fetch('https://reading-t9nr.onrender.com/api/reading-participation')
    const data = await res.json()

    const trace1 = {
      x: data.generations,
      y: data.males,
      name: 'Males',
      type: 'bar',
      marker: { color: 'blue' }
    }

    const trace2 = {
      x: data.generations,
      y: data.females,
      name: 'Females',
      type: 'bar',
      marker: { color: 'pink' }
    }

   const layout = {
  title: 'Participation in Reading by Sex and Generation',
  xaxis: { title: 'Generation' },
  yaxis: { title: 'Participation (%)' },
  barmode: 'group',         
  bargap: 0.2,
  bargroupgap: 0.1,
  template: 'plotly_white',
  width: 700,
  height: 400,
  margin: { t: 50, l: 50, r: 30, b: 50 },
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor: 'rgba(0,0,0,0)'
}


    Plotly.newPlot(chart.value, [trace1, trace2], layout)
  } catch (error) {
    console.error('📉 Failed to load chart data:', error)
  }
})
</script>

<style scoped>
body {
  background-color: #f7f7fc;
}
</style>
