<template>
  <div class="read-section">
    <div class="quiz-container">
      <!-- Title and current word -->
      <h1 class="title">🧠 Synonym Challenge</h1>
      <h2 class="subtitle">
        Choose the correct synonyms for: <strong>{{ wordLists[currentIndex].word }}</strong>
      </h2>

      <!-- Answer options as checkboxes -->
      <div class="word-grid">
        <div v-for="option in wordLists[currentIndex].options" :key="option" class="word-card">
          <label>
            <input type="checkbox" :value="option" v-model="selectedOptions" />
            <span>{{ option }}</span>
          </label>
        </div>
      </div>

      <!-- Submit button: advances to next or shows result -->
      <button class="action-btn" @click="submitChoices">
        {{ currentIndex < wordLists.length - 1 ? '➡️ Next' : '📊 Show Result' }}
      </button>

      <!-- Final result popup -->
      <div class="result-modal" v-if="gameOver">
        <div class="result-card">
          <h2>🎉 Your Results</h2>
          <p>Your Score: <strong>{{ finalScore }} / {{ wordLists.length }}</strong></p>
          <div class="result-actions">
            <button class="btn-primary" @click="restart">🔁 Try Again</button>
            <button class="btn-secondary" @click="gameOver = false">❌ Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

  
<script setup>
import { ref } from 'vue'

// List of quiz questions
const wordLists = [
  {
    word: 'happy',
    options: ['joyful', 'elated', 'depressed', 'annoyed'],
    correctAnswers: ['joyful', 'elated']
  },
  {
    word: 'stuck',
    options: ['cling', 'rift', 'abide', 'cleave'],
    correctAnswers: ['cling', 'abide', 'cleave']
  },
  {
    word: 'toxic',
    options: ['joyful', 'poisonous', 'ethereal', 'venomous'],
    correctAnswers: ['poisonous', 'venomous']
  },
  {
    word: 'upset',
    options: ['disturbance', 'explode', 'rest', 'disruption'],
    correctAnswers: ['disturbance', 'disruption']
  },
  {
    word: 'valour',
    options: ['courage', 'bravery', 'melancholy', 'prowess'],
    correctAnswers: ['courage', 'bravery', 'prowess']
  }
]

// Reactive state
const currentIndex = ref(0)           // Current quiz question
const selectedOptions = ref([])       // Options selected by the user
const finalScore = ref(0)             // Final quiz score
const gameOver = ref(false)           // Whether the quiz has ended

// Handle answer submission
const submitChoices = () => {
  const selected = new Set(selectedOptions.value)
  const correct = new Set(wordLists[currentIndex.value].correctAnswers)

  // Exact match check: all correct, no extra
  const isCorrect =
    selected.size === correct.size &&
    [...selected].every(opt => correct.has(opt))

  if (isCorrect) finalScore.value++

  // Move to next question or finish quiz
  if (currentIndex.value < wordLists.length - 1) {
    currentIndex.value++
    selectedOptions.value = []
  } else {
    gameOver.value = true

    // Save score to localStorage (under today's date)
    const today = new Date().toISOString().split('T')[0]
    const saved = JSON.parse(localStorage.getItem('reading_progress') || '[]')
    let record = saved.find(r => r.date === today)
    if (!record) {
      record = { date: today }
      saved.push(record)
    }
    record.synonymScore = finalScore.value
    localStorage.setItem('reading_progress', JSON.stringify(saved))
  }
}

// Restart the quiz
const restart = () => {
  currentIndex.value = 0
  selectedOptions.value = []
  finalScore.value = 0
  gameOver.value = false
}
</script>

  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Baloo+2&family=Fredoka&display=swap');
  
  .read-section {
    min-height: 100vh;
    background: linear-gradient(to bottom, #fff5e6, #ffd9ec);
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Baloo 2', 'Fredoka', sans-serif;
    padding: 2rem;
  }
  
  .quiz-container {
    background-color: #fffdf5;
    max-width: 800px;
    width: 100%;
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  }
  
  .title {
    font-size: 2.2rem;
    color: #6a4c93;
    margin-bottom: 0.3rem;
  }
  
  .subtitle {
    font-size: 1.2rem;
    color: #555;
    margin-bottom: 1.5rem;
  }
  
  .word-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .word-card {
    background-color: #ffe8f0;
    padding: 1rem;
    border-radius: 12px;
    transition: 0.2s ease;
  }
  
  .word-card:hover {
    background-color: #ffd6e8;
    transform: scale(1.03);
  }
  
  .word-card input[type='checkbox'] {
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
    transition: 0.3s ease;
  }
  .action-btn:hover {
    background-color: #ffc947;
  }
  
  /* Result Modal */
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
    background: #fff;
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.2);
  }
  
  .result-card h2 {
    color: #6a4c93;
  }
  
  .result-actions {
    margin-top: 1.5rem;
    display: flex;
    justify-content: center;
    gap: 1rem;
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
  