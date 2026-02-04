<template>
  <div class="container fade-in">
    <!-- Main Title -->
    <h1>📖 Reading Speed Test</h1>

    <!-- Initial screen before test starts -->
    <div v-if="!testStarted">
      <p class="loading-text">Click below to begin your reading test</p>
      <button @click="startTest" class="btn">▶️ Start Reading</button>
    </div>

    <!-- Test in progress -->
    <div v-else>
      <!-- Visual progress bar -->
      <div class="progress-bar">
        <div class="progress" :style="{ width: ((currentIndex + 1) / 5 * 100) + '%' }"></div>
      </div>

      <!-- Paragraph text with transition -->
      <transition name="slide-fade" mode="out-in">
        <div class="card" :key="currentIndex">
          <p v-if="paragraph.length && paragraph[currentIndex]">
            {{ paragraph[currentIndex].text }}
          </p>
          <p v-else class="loading-text">Loading...</p>
        </div>
      </transition>

      <!-- Start timer button -->
      <div v-if="!readingStarted">
        <button class="btn" @click="beginReading">▶️ Start Timer</button>
      </div>

      <!-- Page indicator -->
      <p class="page-indicator">Page {{ currentIndex + 1 }} of 5</p>

      <!-- Timer display and stop button -->
      <div class="timer">
        <h2>{{ minutes }} : {{ seconds }} : {{ miliseconds }}</h2>
        <button @click="stop" class="btn" :disabled="!readingStarted">⏹️ Stop</button>
      </div>

      <!-- Navigation: Next or View Results -->
      <div class="actions">
        <button
          v-if="currentIndex < 4"
          @click="nextParagraph"
          class="arrow-btn"
          :disabled="readingStarted"
        >
          ➡️
        </button>
        <button
          v-else
          @click="totalResult"
          class="btn"
          :disabled="readingStarted"
        >
          ✅ View your Results!
        </button>
      </div>
    </div>

    <!-- Result popup after test completion -->
    <div v-if="displayPopUp" class="result-popup">
      <div class="popup-content">
        <h3>🎉 Your Results</h3>
        <p>You read at <strong>{{ finalWpm }}</strong> words per minute!</p>
        <button class="btn" @click="tryAgain">🔁 Try Again</button>
        <button class="btn" @click="displayPopUp = false">❌ Close</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const goHome = () => router.push('/')

const testStarted = ref(false)
const readingStarted = ref(false)

let timer = null
let totalTime = 0

const miliseconds = ref(0)
const seconds = ref(0)
const minutes = ref(0)
const totalReadingTime = ref([])
const paragraph = ref([])
const currentIndex = ref(0)
let totalWordCount = 0
const finalWpm = ref(null)
const displayPopUp = ref(false)

const startTimer = () => {
  if (timer) return
  timer = setInterval(() => {
    totalTime += 10
    minutes.value = Math.floor(totalTime / 60000)
    seconds.value = Math.floor((totalTime % 60000) / 1000)
    miliseconds.value = totalTime % 1000
  }, 10)
}

const stop = () => {
  clearInterval(timer)
  timer = null
  totalReadingTime.value.push(totalTime)
  readingStarted.value = false
}

const reset = () => {
  stop()
  miliseconds.value = 0
  seconds.value = 0
  minutes.value = 0
  totalTime = 0
}

onMounted(async () => {
  const response = await axios.get('https://reading-t9nr.onrender.com/api/paragraph')
  paragraph.value = response.data
})

const startTest = () => {
  testStarted.value = true
  readingStarted.value = false
  const currentParagraph = paragraph.value[currentIndex.value].text
  totalWordCount += currentParagraph.trim().split(/\s+/).length
}

const beginReading = () => {
  readingStarted.value = true
  startTimer()
}

const nextParagraph = () => {
  reset()
  currentIndex.value++
  readingStarted.value = false
  const currentParagraph = paragraph.value[currentIndex.value].text
  totalWordCount += currentParagraph.trim().split(/\s+/).length
}

const totalResult = () => {
  const totalMs = totalReadingTime.value.reduce((a, b) => a + b, 0)
  const totalMins = totalMs / 60000
  finalWpm.value = Math.round(totalWordCount / totalMins)
  displayPopUp.value = true

  const today = new Date().toISOString().split('T')[0]
  const saved = JSON.parse(localStorage.getItem('reading_progress') || '[]')
  let record = saved.find(r => r.date === today)
  if (!record) {
    record = { date: today }
    saved.push(record)
  }
  record.readingWPM = finalWpm.value
  localStorage.setItem('reading_progress', JSON.stringify(saved))
}

const tryAgain = async () => {
  paragraph.value = []
  currentIndex.value = 0
  totalReadingTime.value = []
  totalWordCount = 0
  reset()
  finalWpm.value = null
  displayPopUp.value = false
  testStarted.value = false
  readingStarted.value = false

  const response = await axios.get('http://127.0.0.1:5000/api/paragraph')
  paragraph.value = response.data
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2&family=Fredoka&display=swap');

.container {
  max-width: 700px;
  margin: 3rem auto;
  padding: 2rem;
  text-align: center;
  font-family: 'Baloo 2', 'Fredoka', sans-serif;
  background: linear-gradient(to bottom, #fff5e6, #ffd9ec);
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: relative;
}

.back-btn {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  background: none;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  color: #6a4c93;
  font-weight: bold;
  transition: all 0.2s;
}
.back-btn:hover {
  text-decoration: underline;
  color: #333;
}

.progress-bar {
  width: 100%;
  height: 12px;
  background-color: #f3e8ff;
  border-radius: 10px;
  margin-bottom: 1rem;
  overflow: hidden;
}
.progress {
  height: 100%;
  background-color: #a78bfa;
  transition: width 0.4s ease-in-out;
  border-radius: 10px;
}

.card {
  background: #fffbe6;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
  text-align: left;
  min-height: 100px;
}

.page-indicator {
  font-size: 0.95rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #555;
}

.timer h2 {
  font-size: 2rem;
  margin: 1rem 0;
}

.btn {
  padding: 0.6rem 1.2rem;
  background-color: #ffd972;
  color: #333;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin: 0.5rem;
  transition: background-color 0.3s;
}
.btn:hover {
  background-color: #ffc947;
}

.arrow-btn {
  font-size: 2rem;
  background: none;
  border: none;
  cursor: pointer;
}

.result-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(35, 47, 69, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.popup-content {
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
}

.loading-text {
  font-style: italic;
  color: #888;
  font-size: 1rem;
  margin-top: 1rem;
}

.fade-in {
  animation: fadeIn 0.6s ease-in-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.5s ease;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
