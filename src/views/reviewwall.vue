<template>
  <div class="read-section">
    <div class="review-wall">
      <!-- Page Header -->
      <h1>🌟 Public Review Wall</h1>

      <!-- Search bar -->
      <div class="search-area">
        <input v-model="searchQuery" placeholder="Search reviews..." class="search-input" />
      </div>

      <!-- Display filtered reviews -->
      <div class="grid">
        <div v-for="review in filteredReviews" :key="review.id" class="card">
          <!-- Review summary -->
          <h2>{{ review.bookTitle }} {{ review.emoji }}</h2>
          <p>{{ review.reviewText }}</p>
          <p>⭐ Rating: {{ review.rating }}/10</p>

          <!-- Reaction buttons -->
          <div class="reactions">
            <button @click="react(review.id, 'like')">👍 {{ review.reactions.like }}</button>
            <button @click="react(review.id, 'love')">❤️ {{ review.reactions.love }}</button>
            <button @click="react(review.id, 'laugh')">😂 {{ review.reactions.laugh }}</button>
            <button class="delete-btn" @click="deleteReview(review.id)">🗑️ Delete</button>
          </div>

          <!-- Comment section -->
          <div class="comment-section">
            <h3>💬 Comments</h3>
            <!-- List of comments -->
            <div v-if="review.comments && review.comments.length">
              <p v-for="(comment, index) in review.comments" :key="index" class="comment">
                {{ comment.content }}
              </p>
            </div>
            <div v-else class="no-comments">No comments yet.</div>

            <!-- New comment input -->
            <input
              v-model="newComments[review.id]"
              placeholder="Write a comment..."
              class="comment-input"
            />
            <button @click="submitComment(review.id)" class="comment-btn">➤ Submit</button>
          </div>
        </div>
      </div>

      <!-- If no reviews match the search -->
      <div v-if="filteredReviews.length === 0" class="no-results">
        No matching reviews found.
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const API_BASE = 'https://reading-t9nr.onrender.com'

// Reactive states
const reviews = ref([])               // All reviews from server
const searchQuery = ref('')           // Text input from search bar
const newComments = ref({})           // Temporary storage for typed comments

// 🔞 List of filtered words
const toxicWords = [
  "fuck", "shit", "bitch", "asshole", "bastard", "dick", "piss", "crap",
  "slut", "whore", "nigger", "retard", "fag", "faggot", "chink", "tranny",
  "idiot", "stupid", "dumb", "loser", "moron", "ugly", "suck",
  "noob", "n00b", "pwn", "rekt", "kill yourself", "die", "kys", "trash",
  "hate", "kill", "burn", "destroy"
]

// 🧠 Leetspeak matcher patterns
const leetMap = {
  a: '[a@4^]', b: '[b8ß]', c: '[c(¢<]', d: '[d)]', e: '[e3€]', f: '[fƒ]', g: '[g69]', h: '[h#]',
  i: '[i1!|l]', k: '[k<]', l: '[l1|!i]', m: '[mnn]', n: '[n]', o: '[o0°()]', p: '[pþ]',
  q: '[q9]', r: '[r®]', s: '[s5$z]', t: '[t7+†]', u: '[uµv]', v: '[vµu]', w: '[wvv]',
  x: '[x%×✕]', y: '[y¥]', z: '[z2s]'
}

// Convert a toxic word into regex pattern to detect leetspeak
function wordToLeetPattern(word) {
  return '\\b' + word.toLowerCase().split('').map(c => leetMap[c] || c).join('[-_ .]*') + '\\b'
}

// Check if text contains any toxic leetspeak
function containsToxicLeetspeak(text) {
  return toxicWords.some(word => {
    const pattern = new RegExp(wordToLeetPattern(word), 'i')
    return pattern.test(text)
  })
}

// 📥 Fetch all reviews on mount
onMounted(async () => {
  try {
    const res = await axios.get(`${API_BASE}/reviews`)
    reviews.value = res.data
  } catch (error) {
    console.error('❌ Failed to load reviews:', error)
  }
})

// 🔍 Filter reviews by title or review text
const filteredReviews = computed(() => {
  if (!searchQuery.value.trim()) return reviews.value
  const keyword = searchQuery.value.toLowerCase()
  return reviews.value.filter(review =>
    review.bookTitle.toLowerCase().includes(keyword) ||
    review.reviewText.toLowerCase().includes(keyword)
  )
})

// ❤️ React to a review (like, love, laugh)
const react = async (id, type) => {
  try {
    await axios.post(`${API_BASE}/reviews/${id}/react`, { reaction: type })
    const review = reviews.value.find(r => r.id === id)
    if (review) review.reactions[type]++
  } catch (error) {
    console.error('❌ Failed to react:', error)
  }
}

// 💬 Submit a new comment with content filter
const submitComment = async (id) => {
  const content = newComments.value[id]?.trim()
  if (!content) return

  if (containsToxicLeetspeak(content)) {
    alert("❌ Your comment contains inappropriate language.")
    return
  }

  try {
    await axios.post(`${API_BASE}/reviews/${id}/comment`, { content })
    const review = reviews.value.find(r => r.id === id)
    if (review) {
      if (!review.comments) review.comments = []
      review.comments.push({ content })
    }
    newComments.value[id] = ''  // Clear input field
  } catch (error) {
    console.error('❌ Failed to add comment:', error)
  }
}

// 🗑️ Delete a review by ID
const deleteReview = async (id) => {
  try {
    await axios.delete(`${API_BASE}/reviews/${id}`)
    reviews.value = reviews.value.filter(r => r.id !== id)
  } catch (err) {
    console.error('❌ Failed to delete review:', err)
    alert("Delete failed.")
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

.review-wall {
  max-width: 2000px;
  margin: 2rem auto;
  text-align: center;
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

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.card {
  background: #fef8ec;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}
.card:hover {
  transform: rotate(2deg) scale(1.02);
}

.reactions {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}
button {
  background: none;
  border: none;
  cursor: pointer;
}

.delete-btn {
  background-color: #f8d7da;
  border: none;
  padding: 0.3rem 0.8rem;
  border-radius: 8px;
  cursor: pointer;
  margin-left: 0.5rem;
  font-weight: bold;
  color: #721c24;
}

.comment-section {
  margin-top: 1rem;
  text-align: left;
}
.comment {
  background: #fff;
  margin: 0.3rem 0;
  padding: 0.5rem;
  border-radius: 6px;
}
.no-comments {
  font-size: 0.9rem;
  color: gray;
}
.comment-input {
  width: 100%;
  margin-top: 0.5rem;
  padding: 0.4rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}
.comment-btn {
  margin-top: 0.5rem;
  background-color: #ffd972;
  border: none;
  padding: 0.4rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}
.no-results {
  margin-top: 2rem;
  color: gray;
  font-size: 1.1rem;
}
</style>
