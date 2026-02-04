<template>
  <div class="read-section">
    <div class="quiz-container">
      <h1 class="title">🤖 AI Debate Arena</h1>

      <!-- Topic selection section -->
      <div v-if="!topicChosen" class="topic-select">
        <h3 class="subtitle">Select a topic to debate:</h3>
        <div class="word-grid">
          <div
            v-for="t in sampleTopics"
            :key="t"
            class="word-card"
            @click="selectTopic(t)"
          >
            {{ t }}
          </div>
        </div>
      </div>

      <!-- Debate chat section -->
      <div v-else>
        <h2 class="subtitle">Debating: <strong>{{ topic }}</strong></h2>

        <!-- Chat history -->
        <div class="chat-box">
          <div v-for="(msg, i) in chatHistory" :key="i" :class="msg.role">
            <strong>{{ msg.role === 'user' ? 'You' : 'AI' }}:</strong> {{ msg.content }}
          </div>
        </div>

        <!-- Input area for user arguments -->
        <div class="input-area">
          <input
            v-model="userInput"
            placeholder="Enter your argument..."
            @keyup.enter="submitTurn"
          />
          <button class="action-btn" @click="submitTurn">➡️ Send</button>
        </div>

        <!-- Score display -->
        <div v-if="score" class="score-board">
          <p><strong>Relevance:</strong> {{ score.relevance }} / 50</p>
          <p><strong>Complexity:</strong> {{ score.complexity }} / 50</p>
          <p><strong>Total:</strong> {{ score.total }} / 100</p>
        </div>

        <!-- Reset debate button -->
        <div class="result-actions">
          <button class="btn-secondary" @click="resetDebate">🔁 Restart</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

// List of debate topics
const sampleTopics = [
  "Should homework be banned?",
  "Is AI a threat to humanity?",
  "The future of electric cars",
  "Should we colonize Mars?",
  "Are video games good for kids?"
]

// Reactive state variables
const topic = ref('')
const topicChosen = ref(false)
const userInput = ref('')
const chatHistory = ref([])
const score = ref(null)

// Set selected topic and reset states
const selectTopic = (t) => {
  topic.value = t
  topicChosen.value = true
  chatHistory.value = []
  score.value = null
}

// Submit user input and fetch AI response + score
const submitTurn = async () => {
  if (!userInput.value.trim()) return
  chatHistory.value.push({ role: 'user', content: userInput.value })
  try {
    const res = await axios.post('https://reading-t9nr.onrender.com/api/debate-round', {
      topic: topic.value,
      history: chatHistory.value
    })
    score.value = res.data.score
    chatHistory.value.push({ role: 'assistant', content: res.data.reply })
    userInput.value = ''
  } catch (err) {
    console.error(err)
  }
}

// Reset debate state to start over
const resetDebate = () => {
  topicChosen.value = false
  topic.value = ''
  userInput.value = ''
  chatHistory.value = []
  score.value = null
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
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.word-card {
  background-color: #ffe8f0;
  padding: 1rem;
  border-radius: 12px;
  cursor: pointer;
  transition: 0.2s ease;
}

.word-card:hover {
  background-color: #ffd6e8;
  transform: scale(1.03);
}

.chat-box {
  background: #fffdf5;
  padding: 1rem;
  border-radius: 12px;
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 1rem;
  text-align: left;
}

.user {
  text-align: right;
  color: #333;
  margin: 0.5rem 0;
}

.assistant {
  text-align: left;
  color: #6a4c93;
  margin: 0.5rem 0;
}

.input-area {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

input {
  flex: 1;
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.action-btn {
  background-color: #ffd972;
  color: #333;
  font-weight: bold;
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.score-board {
  margin-top: 1rem;
  background-color: #f3f3f3;
  padding: 1rem;
  border-radius: 12px;
  text-align: left;
}

.result-actions {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
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