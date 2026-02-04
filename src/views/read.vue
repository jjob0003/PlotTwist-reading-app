<template>
  <!-- Title Section -->
  <div class="col-md-6 offset-md-3 text-center">
    <h1 class="title-text">Assess Your Reading Skills</h1>
  </div>

  <!-- Visual Interactive Section -->
  <div class="reading-room">
    <div class="image-container">
     
      <!-- Background image for the room -->
      <img src="../assets/readBG.png" alt="Reading Room" class="background-image" />

      <!-- Clickable Hotspot: Generate a Story -->
      <div class="hotspot window-hotspot" @click="goTo('/generate')">
        <div class="tooltip">Generate A Story</div>
      </div>

      <!-- Clickable Hotspot: Take a Quiz -->
      <div class="hotspot book-hotspot" @click="goTo('/quiz')">
        <div class="tooltip">Quiz</div>
      </div>

      <!-- Clickable Hotspot: Reading Speed Test -->
      <div class="hotspot bookshelf-hotspot" @click="goTo('/readingspeedtest')">
        <div class="tooltip">Reading Speed</div>
      </div>

      <!-- Decorative arrows pointing to each hotspot -->
      <img src="/generate.png" alt="generate-arrow" class="generate-arrow-img" />
      <img src="/quiz.png" alt="quiz-arrow" class="quiz-arrow-img" />
      <img src="/speed.png" alt="speed-arrow" class="speed-arrow-img" />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

// Vue Router instance
const router = useRouter()

// Navigate to a specific route when hotspot is clicked
const goTo = (path) => {
  router.push(path)
}
</script>

 
<style scoped>
 
@import url('https://fonts.googleapis.com/css2?family=Baloo+2&family=Fredoka&display=swap');
 
.reading-room {
  min-height: 100vh;
  background-color: rgb(255,253,255);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4rem 2rem;
  font-family: 'Baloo 2', 'Fredoka', sans-serif;
}
 
.image-container {
  position: relative;
  width: 100%;
  max-width: 900px;
}
 
.background-image {
  width: 100%;
  display: block;
  border-radius: 16px;
}
 
 
.hotspot {
  position: absolute;
  cursor: pointer;
  overflow: visible;
  transition: transform 0.4s ease, filter 0.4s ease;
}
 
 
.hotspot:hover {
  transform: scale(1.1);
  filter: brightness(1.1) drop-shadow(0 0 12px rgba(255, 192, 203, 0.6));
}
 
 
.tooltip {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); 
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(5px);
  padding: 0.6rem 1rem;
  border-radius: 12px;
  color: #455540;
  font-weight: bold;
  font-size: 1rem;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
  white-space: nowrap;
  z-index: 10;
}
 
.hotspot:hover .tooltip {
  opacity: 1;
}
 
 
.window-hotspot {
  top: 24%;
  left: 48%;
  width: 30%;
  height: 20%;
}
 
.book-hotspot {
  top: 53%;
  left: 50%;
  width: 22%;
  height: 10%;
}
 
.bookshelf-hotspot {
  top: 33%;
  left: 15%;
  width: 20%;
  height: 18%;
}
.hotspot {
  position: absolute;
  cursor: pointer;
  transition: box-shadow 0.4s ease, filter 0.4s ease;
}
 
 
.hotspot:hover {
  box-shadow: 0 0 20px 8px rgba(255, 223, 249, 0.5);
  filter: brightness(1.1);
}
 
.generate-arrow-img{
  position: absolute;
  height: 210px;
  width: auto;
  top: 15%;
  left: 80%;
  pointer-events: none;
}
 
.quiz-arrow-img{
  position: absolute;
  height: 210px;
  width: auto;
  top: 60%;
  left: 80%;
  pointer-events: none;
}
 
.speed-arrow-img{
  position: absolute;
  height: 210px;
  width: auto;
  top: 20%;
  right: 80%;
  pointer-events: none;
}
 
.title-text{
  font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
  font-size: 30px;
  font-weight: 700;
  margin-top: 3%;
  color: #a25419;
  /* text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black; */
  margin-bottom: -4%;
}
 
</style>
 