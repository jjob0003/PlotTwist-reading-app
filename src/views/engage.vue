<template>
  <div class="reading-room">
    <!-- Page Title -->
    <div>
      <h1 class="title-text">Choose Your Reading Adventure</h1>
    </div>

    <!-- Background image and interactive hotspots -->
    <div class="image-container">
      <!-- Main background image -->
      <img src="/engage.jpg" alt="Reading Room" class="background-image" />

      <!-- Clickable hotspot: leads to Review Wall -->
      <div class="hotspot window-hotspot" @click="goTo('/reviewwall')">
        <div class="tooltip">Review Wall</div>
      </div>

      <!-- Clickable hotspot: leads to Share Review -->
      <div class="hotspot sofa-hotspot" @click="goTo('/sharereview')">
        <div class="tooltip">Share Your Review</div>
      </div>

      <!-- Clickable hotspot: leads to Reading List -->
      <div class="hotspot fireplace-hotspot" @click="goTo('/readinglist')">
        <div class="tooltip">Your Reading List</div>
      </div>

      <!-- Clickable hotspot: leads to Moodboard -->
      <div class="hotspot lamp-hotspot" @click="goTo('/MoodBoardHome')">
        <div class="tooltip">Moodboard</div>
      </div>

      <!-- Decorative arrow icons for each section -->
      <img src="/review.png" alt="generate-arrow" class="review-arrow-img"/>
      <img src="/share.png" alt="share-arrow" class="share-arrow-img"/>
      <img src="/check.png" alt="check-reading-arrow" class="check-reading-arrow-img"/>
      <img src="/moodboard.png" alt="moodboard-arrow" class="moodboard-arrow-img"/>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

// Access router for programmatic navigation
const router = useRouter()

// Navigate to given route path
const goTo = (path) => {
  router.push(path)
}
</script>


<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Baloo+2&family=Fredoka&display=swap');

.reading-room {
  min-height: 100vh;
  background-color: #010b1f;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4rem 2rem;
  font-family: 'Baloo 2', 'Fredoka', sans-serif;
  flex-direction: column;
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
  top: 2%;
  left: 75%;
  width: 25%;
  height: 70%;
}

.sofa-hotspot {
  top: 57%;
  left: 48%;
  width: 30%;
  height: 40%;
}

.fireplace-hotspot {
  top: 60%;
  left: 12%;
  width: 23%;
  height: 30%;
}

.lamp-hotspot{
  top: 15%;
  left: 23%;
  width: 15%;
  height: 30%;
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

.review-arrow-img{
  position: absolute;
  height: 170px;
  width: auto;
  top: 15%;
  left: 80%;
  pointer-events: none;
}

.share-arrow-img{
  position: absolute;
  height: 150px;
  width: auto;
  top: 70%;
  left: 80%;
  pointer-events: none;
}

.check-reading-arrow-img{
  position: absolute;
  height: 210px;
  width: auto;
  top: 66%;
  right: 86%;
  pointer-events: none;
}

.moodboard-arrow-img{
  position: absolute;
  height: 100px;
  width: auto;
  top: 20%;
  right: 74%;
  pointer-events: none;
}

.title-text{
  font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
  font-size: 30px;
  font-weight: 600;
  color: #e38705;
  margin-bottom: 8%;
  margin-top: -4%;
}

</style>