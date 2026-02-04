<template>
  <div class="worlds">
    <!-- Loop through each section and render a clickable world card -->
    <div class="world" v-for="(section, i) in sections" :key="i" @click="goTo(section.link)">
      <!-- Background image -->
      <div class="bg" :style="{ backgroundImage: `url(${section.bg})` }"></div>
      
      <!-- Section title and description -->
      <div class="label">
        <h2>{{ section.title }}</h2>
        <p>{{ section.desc }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()  // Access the Vue Router instance

// Import background images for each section
import bg1 from '../assets/bg1.jpg'
import bg2 from '../assets/bg2.jpg'
import bg3 from '../assets/bg3.jpg'
import bg4 from '../assets/bg4.jpg'

// Define the section content and routing destinations
const sections = [
  {
    title: 'ASSESS',
    desc: 'Evaluate your reading skills through interactive quizzes',
    bg: bg1,
    link: '/read'
  },
  {
    title: 'IMPROVE',
    desc: 'Sharpen comprehension with AI-generated stories & paragraphs',
    bg: bg2,
    link: '/improve'
  },
  {
    title: 'ENGAGE',
    desc: 'Express yourself by uploading images to your mood board',
    bg: bg3,
    link: '/engage'
  },
  {
    title: 'LOCATE',
    desc: 'Track and review your reading performance anytime',
    bg: bg4,
    link: '/result'
  }
]

// Navigate to the path when a section is clicked
const goTo = (path) => {
  router.push(path)
}
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2&family=Fredoka&display=swap');

body {
  font-family: 'Baloo 2', 'Fredoka', sans-serif;
}
.worlds {
  display: flex;
  height: 100vh;
  overflow: hidden;
  font-family: 'Baloo 2', 'Fredoka', sans-serif;
}

.world {
  flex: 1;
  position: relative;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.world:hover {
  transform: scale(1.02);
}

.bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  filter: brightness(0.8);
}

.label {
  position: absolute;
  bottom: 2rem;
  left: 1rem;
  color: white;
  z-index: 2;
  text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
}

.label h2 {
  font-size: 2rem;
  margin: 0;
}

.label p {
  font-size: 1rem;
  opacity: 0.8;
}
</style>
