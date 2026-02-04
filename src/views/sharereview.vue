<template>
  <div class="read-section">
    <div class="container">

      <!-- Page Header -->
      <h1 class="title">📚 Share a Review</h1>

      <!-- Book search bar -->
      <div class="search-area">
        <input v-model="searchQuery" placeholder="Search books..." class="search-input" />
      </div>

      <!-- Display list of books to select from -->
      <div class="preset-books">
        <div
          v-for="book in filteredBooks"
          :key="book.key"
          class="book-card"
          @click="selectBook(book)"
        >
          <p>{{ book.title }}</p>
        </div>
      </div>

      <!-- Review form: appears only when a book is selected -->
      <div v-if="selectedBook" class="review-form">
        <h2 class="selected-title">✍️ Reviewing: {{ selectedBook.title }}</h2>

        <!-- Review text input -->
        <div class="card">
          <textarea
            v-model="reviewText"
            placeholder="Write your review (max 300 characters)"
            maxlength="300"
            class="textarea"
          ></textarea>
          <div class="info">Characters left: {{ 300 - reviewText.length }}</div>
        </div>

        <!-- Emoji selector -->
        <div class="card">
          <select v-model="selectedEmoji" class="search-input">
            <option disabled value="">Select an emoji</option>
            <option>😊</option>
            <option>📖</option>
            <option>💭</option>
            <option>🌟</option>
            <option>🤔</option>
          </select>
        </div>

        <!-- Numeric rating input (1 to 10) -->
        <div class="card">
          <input
            v-model.number="rating"
            type="number"
            min="1"
            max="10"
            placeholder="Rating (1-10)"
            class="search-input"
          />
        </div>

        <!-- Submit button with validation -->
        <div class="card">
          <button
            :disabled="!isReviewValid"
            @click="submitReview"
            class="btn"
          >
            ✅ Post Review
          </button>
          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        </div>

        <!-- Disclaimer -->
        <p class="disclaimer">
          Your review is posted anonymously and safely stored.
        </p>
      </div>

      <!-- Toast message for feedback (e.g., "Posted!") -->
      <div v-if="toastMessage" class="toast">
        {{ toastMessage }}
      </div>

    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const API_BASE = 'https://reading-t9nr.onrender.com'


const presetBooks = ref([])
const searchQuery = ref('')
const selectedBook = ref(null)
const reviewText = ref('')
const selectedEmoji = ref('')
const rating = ref(null)
const errorMessage = ref('')
const toastMessage = ref('')
const router = useRouter()


const filteredBooks = computed(() => {
  if (!searchQuery.value.trim()) return presetBooks.value
  return presetBooks.value.filter(book =>
    book.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const selectBook = (book) => {
  selectedBook.value = book
}


let toastTimer = null
const showToast = (message) => {
  toastMessage.value = message
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    toastMessage.value = ''
  }, 2000)
}


const checkTone = (text) => {
  const bannedWords = ['bad', 'hate', 'stupid', 'ugly', 'kill']
  const lowered = text.toLowerCase()
  return !bannedWords.some(word => lowered.includes(word))
}


const isReviewValid = computed(() =>
  selectedBook.value && reviewText.value && selectedEmoji.value && rating.value &&
  checkTone(reviewText.value)
)


const submitReview = async () => {
  if (!checkTone(reviewText.value)) {
    errorMessage.value = '❌ Your review must be neutral and constructive.'
    return
  }

  try {
    await axios.post(`https://reading-t9nr.onrender.com/reviews`, {
      bookTitle: selectedBook.value.title,
      reviewText: reviewText.value,
      emoji: selectedEmoji.value,
      rating: rating.value
    })

    selectedBook.value = null
    reviewText.value = ''
    selectedEmoji.value = ''
    rating.value = null
    errorMessage.value = ''

    showToast('✅ Review Posted!')
    setTimeout(() => {
      router.push('/reviewwall')
    }, 1000)
  } catch (error) {
    console.error('Error posting review:', error)
    errorMessage.value = error.response?.data?.error || '❌ Failed to post review.'
  }
}

onMounted(async () => {
  try {
    const res = await axios.get(`${API_BASE}/api/books`)
    presetBooks.value = res.data
  } catch (err) {
    console.error('❌ Failed to load books:', err)
  }
})
</script>


<style scoped>
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
  max-width: 900px;
  margin: 2rem auto;
  padding: 1rem;
}
.title {
  font-size: 2rem;
  text-align: center;
  color: #6a4c93;
  margin-bottom: 2rem;
}
.search-area {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}
.search-input {
  width: 60%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.preset-books {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  gap: 1rem;
  padding-bottom: 1rem;
  scroll-snap-type: x mandatory;
}
.preset-books::-webkit-scrollbar {
  height: 8px;
}
.preset-books::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 4px;
}
.preset-books::-webkit-scrollbar-track {
  background: transparent;
}
.book-card {
  flex: 0 0 auto;
  width: 180px;
  background: #fef8ec;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: center;
  cursor: pointer;
  scroll-snap-align: start;
  transition: transform 0.3s ease;
}
.book-card:hover {
  transform: scale(1.05);
}
.review-form {
  margin-top: 2rem;
}
.selected-title {
  text-align: center;
  margin-bottom: 1rem;
  color: #6a4c93;
}
.card {
  background: #fef8ec;
  margin: 1rem 0;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.textarea {
  width: 100%;
  height: 100px;
  resize: none;
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-family: inherit;
}
.btn {
  width: 100%;
  padding: 0.7rem;
  background-color: #ffd972;
  color: black;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.btn:disabled {
  background-color: #ccc;
}
.info {
  font-size: 0.9rem;
  color: gray;
  margin-top: 0.5rem;
}
.error {
  color: red;
  margin-top: 0.5rem;
}
.disclaimer {
  font-size: 0.8rem;
  color: #777;
  text-align: center;
  margin-top: 2rem;
}
.toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #4caf50;
  color: white;
  padding: 0.8rem 1.5rem;
  border-radius: 20px;
  font-size: 1rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  animation: fadeInOut 2s;
}
@keyframes fadeInOut {
  0% { opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { opacity: 0; }
}
</style>
