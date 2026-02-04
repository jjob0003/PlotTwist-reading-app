<template>
  <div>
    <!-- Floating Button to toggle chat visibility -->
    <button class="chat-fab" @click="visible = !visible">💬</button>

    <!-- Chat Box -->
    <div class="chatbox" v-if="visible">
      <!-- Chat Header -->
      <div class="chat-header">
        🤖 BookBot
        <span @click="visible = false" class="close-btn">❌</span>
      </div>

      <!-- Message Display -->
      <div class="chat-body">
        <div v-for="(msg, index) in messages" :key="index" :class="msg.role">
          <p>{{ msg.content }}</p>
        </div>
      </div>

      <!-- Input Area -->
      <div class="chat-footer">
        <input
          v-model="input"
          @keyup.enter="send"
          placeholder="Ask about this website..."
        />
        <button @click="send">➤</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// State variables
const visible = ref(false)             // Chat box visibility
const input = ref('')                  // User input
const initialized = ref(false)         // Flag to check if assistant is initialized
const messages = ref([
  { role: 'bot', content: '👋 Please wait while I load the assistant...' }
])

// Load assistant when component is mounted
onMounted(async () => {
  try {
    const res = await axios.post('https://reading-t9nr.onrender.com/api/sitechat', {
      message: 'Farting'   // First dummy message to initialize backend
    })
    messages.value.push({ role: 'bot', content: res.data.reply })
    initialized.value = true
  } catch (err) {
    messages.value.push({ role: 'bot', content: '❌ Failed to initialize assistant.' })
  }
})

// Send user message and get bot reply
const send = async () => {
  if (!input.value.trim() || !initialized.value) return

  // Save user message
  const userMessage = { role: 'user', content: input.value }
  messages.value.push(userMessage)
  const inputCopy = input.value
  input.value = ''

  try {
    const res = await axios.post('https://reading-t9nr.onrender.com/api/sitechat', {
      message: inputCopy
    })
    messages.value.push({ role: 'bot', content: res.data.reply })
  } catch (err) {
    messages.value.push({ role: 'bot', content: '❌ Sorry, something went wrong.' })
  }
}
</script>



<style scoped>
.chat-fab {
  position: fixed;
  bottom: 24px;
  right: 24px;
  font-size: 1.5rem;
  border: none;
  background: #6a4c93;
  color: white;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  cursor: pointer;
}

.chatbox {
  position: fixed;
  bottom: 100px;
  right: 24px;
  width: 320px;
  max-height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  z-index: 999;
}

.chat-header {
  background: #6a4c93;
  color: white;
  padding: 10px;
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}

.close-btn {
  cursor: pointer;
}

.chat-body {
  padding: 10px;
  flex: 1;
  overflow-y: auto;
  font-size: 0.9rem;
}

.user {
  text-align: right;
  color: #333;
  margin: 6px 0;
}

.bot {
  text-align: left;
  color: #6a4c93;
  margin: 6px 0;
}

.chat-footer {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ccc;
}

.chat-footer input {
  flex: 1;
  padding: 6px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.chat-footer button {
  background: #ffd972;
  border: none;
  margin-left: 8px;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: bold;
}
</style>
