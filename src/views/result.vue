<template>
    <div class="read-section">
      <h1 class="title">📈 Your Progress Over Time</h1>
  
      <div v-if="!history.length" class="empty">
        No progress data yet. Come back after trying some reading activities!
      </div>
  
      <table v-else class="progress-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>WPM</th>
            <th>Vocab Level</th>
            <th>Vocab Score</th>
            <th>Synonym Score</th>
            <th>Quiz</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in history" :key="record.date">
            <td>{{ record.date }}</td>
            <td>{{ record.readingWPM ?? '-' }}</td>
            <td>{{ record.vocabLevel ?? '-' }}</td>
            <td>{{ record.vocabScore ?? '-' }}</td>
            <td>{{ record.synonymScore ?? '-' }}/5</td>
            <td v-if="record.quizTotal">{{ record.quizScore }}/{{ record.quizTotal }}</td>
            <td v-else>-</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  
  const history = ref([])
  
  onMounted(() => {
    const saved = localStorage.getItem('reading_progress')
    if (saved) {
      history.value = JSON.parse(saved).sort((a, b) => b.date.localeCompare(a.date))
    }
  })
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Baloo+2&family=Fredoka&display=swap');
  
  .read-section {
    min-height: 100vh;
    background: linear-gradient(to bottom, #fff5e6, #ffd9ec);
    padding: 4rem 2rem;
    font-family: 'Baloo 2', 'Fredoka', sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .title {
    font-size: 2rem;
    color: #6a4c93;
    margin-bottom: 2rem;
  }
  
  .empty {
    font-size: 1.2rem;
    color: #999;
  }
  
  .progress-table {
    width: 100%;
    max-width: 900px;
    border-collapse: collapse;
    background: #fffdf5;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
    border-radius: 12px;
    overflow: hidden;
  }
  
  th, td {
    padding: 1rem;
    border-bottom: 1px solid #eee;
    text-align: center;
    font-size: 1rem;
  }
  
  th {
    background-color: #f3e8ff;
    color: #6a4c93;
  }
  </style>
  