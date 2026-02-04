<template>
  <div
    class="spider-helper"
    :style="{ top: position.y + 'px', left: position.x + 'px' }"
    @mousedown="startDrag"
  >
    <img :src="spiderImage" alt="Spider" class="spider-img" />
    <div class="spider-bubble">{{ message }}</div>
  </div>
</template>
 
<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import spiderImage from '../assets/spider1.png'
 
const route = useRoute()
const position = ref({ x: 10, y: 60 })
let isDragging = false
let offsetX = 0
let offsetY = 0
 
const startDrag = (e) => {
  isDragging = true
  offsetX = e.clientX - position.value.x
  offsetY = e.clientY - position.value.y
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
}
 
const onDrag = (e) => {
  if (!isDragging) return
  position.value.x = e.clientX - offsetX
  position.value.y = e.clientY - offsetY
}
 
const stopDrag = () => {
  isDragging = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}
 
onBeforeUnmount(() => {
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
})
 
const message = computed(() => {
  if (route.path.includes('MoodBoard')) return 'Welcome to the Moodboard.Upload images and quotes to visually express your ideas.Arrange freely, customize your layout, and export as a PDF.Start creating your board now.'
  if (route.path.includes('readingstatus')) return 'We used to read for fun. Now we scroll for hours. See the twist?'
   if (route.path.includes('readinglist')) return 'Add books you want to read, dropped, or loved — organize your reading journey!'
  if (route.path.includes('read')) return 'Try clicking on the window, books, or shelf to explore stories!'
  if (route.path.includes('generate')) return 'Enter a keyword you like and we’ll generate a story and some questions for you.'
  if (route.path.includes('readingspeed') || route.path.includes('readingspeedtest')) {
    return 'You’ll read five passages here. We’ll calculate your reading time and words per minute.'
  }
  if (route.path.includes('quiz')) return 'Pick the words you know — challenge your vocabulary!'
  if (route.path.includes('SynonymGame')) return 'Select the word that best matches the meaning — a synonym game!'
  if (route.path.includes('aidebate')) return 'Debate with AI and get a score based on your argument!'
 
  if (route.path.includes('sharereview')) return 'Choose a book and share your review — post it to the review wall!'
  if (route.path.includes('reviewwall')) return 'Here you can view all user reviews. Feel free to like or comment!'
 
  return 'Welcome! Start your reading adventure from here!'
})
</script>
 
<style scoped>
.spider-helper {
  position: fixed;
  z-index: 1000;
  display: flex;
  align-items: center;
  cursor: grab;
  user-select: none;
}
 
.spider-img {
  width: 50px;
  height: 50px;
  margin-right: 8px;
}
 
.spider-bubble {
  background: #c9c7bc;
  /* background: #d2dfc3; */
  border: 1px solid #637846;
  padding: 8px 12px;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  font-size: 0.9rem;
  max-width: 200px;
}
</style>