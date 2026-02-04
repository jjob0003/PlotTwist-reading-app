<template>
  <!-- Only show back button if the current route is not in the excluded list -->
  <button v-if="shouldShow" class="back-btn" @click="goHome">🔙 Back to Home</button>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { computed } from 'vue'

const router = useRouter()   // Access the router instance
const route = useRoute()     // Access the current route info

// Navigate to the home page when button is clicked
const goHome = () => router.push('/home')

// Define routes where the back button should NOT be shown
const excludedRoutes = ['/', '/home', '/readingstatus']

// Compute whether to show the back button based on current route
const shouldShow = computed(() => !excludedRoutes.includes(route.path))
</script>

  
  <style scoped>
  .back-btn {
    position: fixed;
    top: 1.5rem;
    left: 1.5rem;
    background: none;
    border: none;
    font-size: 1rem;
    cursor: pointer;
    color: #6a4c93;
    font-weight: bold;
    z-index: 9999;
    transition: all 0.2s;
  }
  .back-btn:hover {
    text-decoration: underline;
    color: #333;
  }
  </style>
  