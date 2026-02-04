<template>
  <div class="read-section">
    <div class="quiz-container">
      <h1 class="title">🧠 Vocabulary Challenge</h1>
      <h2 class="subtitle">Level {{ level }} - Choose the words you know!</h2>
  
      <div class="word-grid">
        <div v-for="word in getCurrentList()" :key="word" class="word-card">
          <label>
            <input type="checkbox" :value="word" v-model="selectedWords" />
            <span>{{ word }}</span>
          </label>
        </div>
      </div>
  
      <button class="action-btn" @click="submitSelectedWords">
        {{ level < 3 ? '➡️ Continue' : '📊 Show Result' }}
      </button>
  
      <!-- Final result modal -->
      <div class="result-modal" v-if="displayPopUp">
        <div class="result-card">
          <h2>🎉 Vocabulary Test Result</h2>
          <p>Your Level: <strong>{{ finalVocabLevel }}</strong></p>
          <p>Total Score: <strong>{{ finalScoreCount }}</strong></p>
          <div class="result-actions">
            <button class="btn-primary" @click="tryAgain">🔁 Try Again</button>
            <button class="btn-secondary" @click="displayPopUp = false">❌ Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  </template>
  
<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Current difficulty level (1 = easy, 2 = medium, 3 = hard)
const level = ref(1)

// Words selected in the current step
const selectedWords = ref([])

// Store selected words per difficulty level
const selectedEasyWords = ref([])
const selectedMediumWords = ref([])
const selectedHardWords = ref([])

// Lists of available words for each level
const easyList = ref([])
const mediumList = ref([])
const hardList = ref([])

// Load word lists from API on component mount
onMounted(async () => {
  const res = await axios.get('https://reading-t9nr.onrender.com/api/words')
  easyList.value = res.data.easy
  mediumList.value = res.data.medium
  hardList.value = res.data.hard
})

// Get current word list based on current level
const getCurrentList = () => {
  if (level.value === 1) return easyList.value
  if (level.value === 2) return mediumList.value
  return hardList.value
}

// Final result state
const finalVocabLevel = ref('')     // "Beginner", "Intermediate", or "Advanced"
const finalScoreCount = ref(0)      // Total score
const displayPopUp = ref(false)     // Controls result popup visibility

// Called when user submits selected words for the current level
const submitSelectedWords = () => {
  if (level.value === 1) {
    selectedEasyWords.value.push(...selectedWords.value)
    level.value++ // Move to medium
  } else if (level.value === 2) {
    selectedMediumWords.value.push(...selectedWords.value)
    level.value++ // Move to hard
  } else {
    selectedHardWords.value.push(...selectedWords.value)
    calculateResult() // All levels done
  }
  selectedWords.value = [] // Reset selection
}

// Calculate score and assign vocabulary level
const calculateResult = () => {
  const score = selectedEasyWords.value.length * 1 +
                selectedMediumWords.value.length * 2 +
                selectedHardWords.value.length * 3

  let levelLabel = 'Beginner'
  if (score > 20) levelLabel = 'Advanced'
  else if (score > 10) levelLabel = 'Intermediate'

  finalVocabLevel.value = levelLabel
  finalScoreCount.value = score
  displayPopUp.value = true

  // Save result to localStorage under today's date
  const today = new Date().toISOString().split('T')[0]
  const saved = JSON.parse(localStorage.getItem('reading_progress') || '[]')
  let record = saved.find(r => r.date === today)
  if (!record) {
    record = { date: today }
    saved.push(record)
  }
  record.vocabScore = finalScoreCount.value
  record.vocabLevel = finalVocabLevel.value
  localStorage.setItem('reading_progress', JSON.stringify(saved))
}

// Reset the quiz to start again
const tryAgain = () => {
  level.value = 1
  selectedWords.value = []
  selectedEasyWords.value = []
  selectedMediumWords.value = []
  selectedHardWords.value = []
  finalVocabLevel.value = ''
  finalScoreCount.value = 0
  displayPopUp.value = false
}
</script>

  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Baloo+2&family=Fredoka&display=swap');
  .read-section {
    min-height: 100vh;
    background: linear-gradient(to bottom, #fff5e6, #ffd9ec);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 4rem 2rem;
    font-family: 'Baloo 2', 'Fredoka', sans-serif;
  }
  .quiz-container {
    font-family: 'Baloo 2', 'Fredoka', sans-serif;
    max-width: 800px;
    margin: 2rem auto;
    padding: 2rem;
    text-align: center;
    background-color: #fffdf5;
    border-radius: 16px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  }
  
  .title {
    font-size: 2rem;
    color: #6a4c93;
    margin-bottom: 0.5rem;
  }
  
  .subtitle {
    font-size: 1.2rem;
    margin-bottom: 1.5rem;
    color: #555;
  }
  
  .word-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .word-card {
    background-color: #ffe8f0;
    border-radius: 12px;
    padding: 1rem;
    transition: all 0.2s ease;
  }
  
  .word-card:hover {
    background-color: #ffd6e8;
    transform: scale(1.03);
  }
  
  .word-card input[type="checkbox"] {
    margin-right: 0.5rem;
  }
  
  .action-btn {
    background-color: #ffd972;
    color: #333;
    font-weight: bold;
    padding: 0.8rem 2rem;
    border: none;
    border-radius: 20px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  .action-btn:hover {
    background-color: #ffc947;
  }
  
  /* Result modal styles */
  .result-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(35, 47, 69, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .result-card {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.2);
  }
  
  .result-card h2 {
    color: #6a4c93;
  }
  
  .result-actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 1.5rem;
  }
  
  .btn-primary {
    background-color: #42b883;
    color: white;
    padding: 0.6rem 1.5rem;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
  }
  
  .btn-secondary {
    background-color: #e0e0e0;
    color: #333;
    padding: 0.6rem 1.5rem;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
  }
  </style>
  