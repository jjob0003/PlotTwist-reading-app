<template>
  <div class="read-section">
    <div class="container">
      <!-- Page title -->
      <h1 class="title">📚 Pick a Book to Add</h1>

      <!-- Book search input -->
      <div class="search-area">
        <input v-model="searchQuery" placeholder="Search books..." class="search-input" />
      </div>

      <!-- Preset books to browse and add -->
      <div class="preset-books">
        <div v-for="book in filteredBooks" :key="book.key" class="book-card">
          <p>{{ book.title }}</p>
          <p>Author: {{ book.author }}</p>
          <p>Rating: ⭐ {{ book.rating }}</p>
          <button @click="addToList(book, 'To Read')" class="add-btn">➕ Add to 'To Read'</button>
        </div>
      </div>

      <!-- Display reading list by status -->
      <div v-for="(books, status) in readingList" :key="status" class="list-section">
        <h2>{{ status }} 📖</h2>
        <div v-if="books.length">
          <div v-for="book in books" :key="book.key" class="book-card">
            <p>{{ book.title }} {{ book.emoji || '' }}</p>
            <!-- Change reading status -->
            <select v-model="book.status" @change="updateStatus(book)">
              <option value="To Read">To Read</option>
              <option value="Reading">Reading</option>
              <option value="Dropped">Dropped</option>
              <option value="Loved">Loved</option>
              <option value="recommendation">recommendation</option>
            </select>
            <button @click="removeBook(book)" class="delete-btn">🗑️ Remove</button>
          </div>
        </div>
        <p v-else>No books in this section yet.</p>
      </div>

      <!-- Button to trigger recommendations -->
      <div class="recommend-section">
        <button @click="getRecommendations" class="recommend-btn">🎯 Get Recommendations</button>
      </div>

      <!-- Recommended books from backend -->
      <div v-if="recommendedBooks.length" class="recommend-results">
        <h2>🔮 Recommended For You</h2>
        <div v-for="book in recommendedBooks" :key="book.book_id" class="book-card">
          <p><strong>{{ book.title }}</strong></p>
        </div>
      </div>

      <!-- Toast notification -->
      <div v-if="toastMessage" class="toast">
        {{ toastMessage }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// Book data and search
const presetBooks = ref([])
const searchQuery = ref('')
const recommendedBooks = ref([])

// Reading list organized by status
const readingList = ref({
  'To Read': [],
  'Reading': [],
  'Dropped': [],
  'Loved': [],
  'recommendation': []
})

// Toast message and timer
const toastMessage = ref('')
let toastTimer = null

// Display toast message for 2 seconds
const showToast = (message) => {
  toastMessage.value = message
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    toastMessage.value = ''
  }, 2000)
}

// Load book list and reading list from localStorage when mounted
onMounted(async () => {
  const savedList = localStorage.getItem('readingList')
  if (savedList) {
    readingList.value = JSON.parse(savedList)
  }

  try {
    const res = await fetch('https://reading-t9nr.onrender.com/api/books')
    const books = await res.json()
    presetBooks.value = books
  } catch (err) {
    console.error('Failed to fetch books:', err)
  }
})

// Filter books based on search query
const filteredBooks = computed(() => {
  if (!searchQuery.value.trim()) {
    return presetBooks.value
  }
  return presetBooks.value.filter(book =>
    book.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// Save the reading list to localStorage
const saveList = () => {
  localStorage.setItem('readingList', JSON.stringify(readingList.value))
}

// Add book to specified status list
const addToList = (book, status) => {
  if (readingList.value[status].some(b => b.key === book.key)) {
    showToast('⚠️ Book already added!')
    return
  }
  readingList.value[status].push({ ...book, status: status, emoji: '' })
  saveList()
  showToast('✅ Book added to list!')
}

// Move book to another status group
const updateStatus = (book) => {
  for (const status in readingList.value) {
    const index = readingList.value[status].findIndex(b => b.key === book.key)
    if (index !== -1) {
      const [movedBook] = readingList.value[status].splice(index, 1)
      movedBook.status = book.status
      readingList.value[book.status].push(movedBook)
      break
    }
  }
  saveList()
  showToast('🔄 Status updated!')
}

// Remove a book from any list
const removeBook = (book) => {
  for (const status in readingList.value) {
    const index = readingList.value[status].findIndex(b => b.key === book.key)
    if (index !== -1) {
      readingList.value[status].splice(index, 1)
      saveList()
      showToast('🗑️ Book removed!')
      break
    }
  }
}

// Fetch book recommendations based on 'Loved' books
const getRecommendations = async () => {
  const lovedBooks = readingList.value['Loved'] || []
  const lovedIds = lovedBooks.map(book => book.key)
  if (lovedIds.length === 0) {
    showToast("🧐 Add some books to 'Loved' first!")
    return
  }

  try {
    const res = await axios.post('https://reading-t9nr.onrender.com/api/recommend', {
      book_ids: lovedIds
    })
    recommendedBooks.value = res.data
    showToast('✨ Recommendations ready!')
  } catch (error) {
    console.error('❌ Recommendation failed:', error)
    showToast('❌ Failed to get recommendations.')
  }
}
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
  width: 200px;
  background: #fef8ec;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: center;
  scroll-snap-align: start;
}
.list-section {
  margin-top: 2rem;
}
.add-btn {
  margin-top: 0.5rem;
  background-color: #d8f3dc;
  border: none;
  padding: 0.3rem 0.8rem;
  border-radius: 8px;
  cursor: pointer;
}
.delete-btn {
  margin-top: 0.5rem;
  background-color: #f8d7da;
  border: none;
  padding: 0.3rem 0.8rem;
  border-radius: 8px;
  cursor: pointer;
  margin-left: 0.5rem;
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
.list-section > div {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
}

</style>
