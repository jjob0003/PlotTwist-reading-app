<template>
  <div class="read-section">
    <div class="container">

      <!-- Title -->
      <h1>📖 Create a fun story!</h1>

      <!-- Keyword input and generate button -->
      <div class="input-area">
        <input v-model="keywords" placeholder="Enter 1–2 fun words!" class="input" />
        <button @click="generateText" class="btn">🎈 Generate</button>
      </div>

      <!-- Loading indicator -->
      <p v-if="loading" class="loading-text">⏳ Generating story and questions...</p>

      <!-- Generated story paragraph -->
      <div v-if="paragraph && !loading" class="card fade-in">
        <h2>📚 Story:</h2>
        <p>{{ paragraph }}</p>
      </div>

      <!-- Generated questions -->
      <div v-if="questions.length && !loading" class="fade-in">
        <h2>🧠 Questions:</h2>
        <div v-for="(q, i) in questions" :key="i" class="card">
          <p>{{ i + 1 }}. {{ q.question }}</p>

          <!-- Multiple choice options -->
          <div v-for="opt in q.options" :key="opt">
            <label>
              <input
                type="radio"
                :name="'q' + i"
                :value="opt.split('.')[0]"
                v-model="userAnswers[i]"
              />
              {{ opt }}
            </label>
          </div>
        </div>
        <!-- Submit button -->
        <button @click="submitAnswers" class="btn">✅ Submit</button>
      </div>

      <!-- Score display -->
      <div v-if="score !== null && !loading" class="score-message">
        🏆 You got {{ score }} / {{ questions.length }}!
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

// Navigation router (not used in current template)
const router = useRouter()
const goBack = () => router.back()

// Reactive variables
const keywords = ref('')
const paragraph = ref('')
const questions = ref([])
const loading = ref(false)
const userAnswers = ref({})
const score = ref(null)

// Generate story + quiz based on keywords
const generateText = async () => {
  if (!keywords.value.trim()) {
    alert("Please enter keywords")
    return
  }

  loading.value = true
  paragraph.value = ''
  questions.value = []
  score.value = null
  userAnswers.value = {}

  try {
    const res = await axios.post('https://reading-t9nr.onrender.com/generate', {
      keywords: keywords.value
    })
    paragraph.value = res.data.paragraph
    questions.value = res.data.questions
  } catch (err) {
    console.error(err)
    alert("Generation failed.")
  } finally {
    loading.value = false
  }
}

// Submit answers and calculate score
const submitAnswers = () => {
  let total = 0
  questions.value.forEach((q, i) => {
    if (userAnswers.value[i] === q.correct) {
      total += 1
    }
  })
  score.value = total

  // Save today's score to localStorage
  const today = new Date().toISOString().split('T')[0]
  const saved = JSON.parse(localStorage.getItem('reading_progress') || '[]')
  let record = saved.find(r => r.date === today)
  if (!record) {
    record = { date: today }
    saved.push(record)
  }
  record.quizScore = score.value
  record.quizTotal = questions.value.length
  localStorage.setItem('reading_progress', JSON.stringify(saved))
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
  
.container {
  max-width: 700px;
  margin: 2rem auto;
  padding: 2rem;
  font-family: 'Baloo 2', 'Fredoka', sans-serif;
  text-align: center;
}

.back-btn {
  background-color: transparent;
  border: none;
  font-size: 1rem;
  color: #555;
  cursor: pointer;
  margin-bottom: 1rem;
  transition: color 0.2s;
}
.back-btn:hover {
  color: #000;
  text-decoration: underline;
}

.input-area {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.input {
  padding: 0.5rem;
  font-size: 1rem;
  width: 60%;
  border: 2px solid #a0d3ff;
  border-radius: 8px;
}

.btn {
  padding: 0.5rem 1rem;
  background-color: #ffd972;
  color: #333;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn:hover {
  background-color: #ffc947;
}

.card {
  background: #fffbe6;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  margin-bottom: 1.5rem;
  text-align: left;
}

.score-message {
  font-size: 1.5rem;
  color: #42b883;
  font-weight: bold;
  margin-top: 1.5rem;
}

.fade-in {
  animation: fadeIn 0.6s ease-in-out;
}

.loading-text {
  font-size: 1.1rem;
  color: #888;
  margin-top: 1rem;
  animation: pulse 1.5s infinite;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}
</style>
