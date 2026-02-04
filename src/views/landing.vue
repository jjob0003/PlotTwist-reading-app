<template>
  <!-- Fullscreen container with background image -->
  <div class="landing-container" :style="{ backgroundImage: `url(${backgroundImage})` }">
    
    <!-- Password prompt overlay (shown only if not authenticated) -->
    <div v-if="!authenticated" class="password-overlay">
      <div class="password-box">
        <h2>🔒 Enter Password</h2>
        <input v-model="inputPassword" type="password" placeholder="Enter password..." />
        <button @click="checkPassword">Submit</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </div>
    </div>

    <!-- Main content shown only after correct password -->
    <div v-else class="overlay">
      <div class="content-box">
        <h1 class="logo-title">PlotTwist</h1>
        <p class="subtitle">Where imagination begins.</p>
        <!-- Navigation buttons -->
        <button class="start-button" @click="router.push('/home')">
          🌟 Let's Begin
        </button>
        <button class="start-button" @click="router.push('/readingstatus')">
          About our webiste
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import backgroundImage from '../assets/bwreading.jpg' // Background image asset

const router = useRouter()

// Simple password-based access control
const correctPassword = '123456'        // Hardcoded correct password
const inputPassword = ref('')           // User input
const authenticated = ref(false)        // Flag to track access state
const errorMessage = ref('')            // Error message display

// Validate password
const checkPassword = () => {
  if (inputPassword.value === correctPassword) {
    authenticated.value = true
    errorMessage.value = ''
  } else {
    errorMessage.value = '❌ Wrong password, try again!'
  }
}
</script>


<style scoped>

.landing-container {
  height: 100vh;
  width: 100vw;
  background-size: cover;
  background-position: center;
  position: relative;
}

.overlay {
  height: 100%;
  width: 100%;
  backdrop-filter: brightness(0.6);
  display: flex;
  align-items: center;
  justify-content: center;
}

.content-box {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 3rem 4rem;
  text-align: center;
  box-shadow: 0 8px 32px rgba(0,0,0,0.25);
  color: white;
  backdrop-filter: blur(8px);
}

.logo-title {
  font-size: 4rem;
  font-weight: bold;
  color: #a682ff;
}

.subtitle {
  font-size: 1.2rem;
  margin-top: 0.5rem;
  margin-bottom: 2rem;
  color: #eee;
}

.start-button {
  padding: 0.8rem 2rem;
  font-size: 1.2rem;
  background-color: #ffd700;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.start-button:hover {
  transform: scale(1.05);
}


.password-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(35, 47, 69, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.password-box {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  text-align: center;
}

.password-box input {
  padding: 0.5rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.password-box button {
  background-color: #6a4c93;
  color: white;
  padding: 0.6rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.password-box .error {
  margin-top: 0.5rem;
  color: red;
}
</style>
