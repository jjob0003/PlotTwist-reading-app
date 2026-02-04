<template>
  <div class="reading-room">
    <div class="image-container">
      <img src="../assets/improve.png" alt="Reading Room" class="background-image" />

      <div class="hotspot synonym-hotspot" @click="goTo('/SynonymGame')">
        <div class="tooltip">Synonym Game</div>
      </div>

      <div class="hotspot debate-hotspot" @click="goTo('/aidebate')">
        <div class="tooltip">Debate with AI</div>
      </div>
      <div class="hotspot phoenetics-hotspot" @click="goTo('/phoeneticsQuiz')">
        <div class="tooltip">How's your phoenetics?</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const goTo = (path) => {
  router.push(path)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2&family=Fredoka&display=swap');

.reading-room {
  min-height: 100vh;
  background-color: #fefefe;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4rem 2rem;
  font-family: 'Baloo 2', 'Fredoka', sans-serif;
}

.image-container {
  position: relative;
  width: 100%;
  max-width: 950px;
}

.background-image {
  width: 100%;
  display: block;
  border-radius: 16px;
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


.tooltip {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(5px);
  padding: 0.6rem 1rem;
  border-radius: 12px;
  color: #6a4c93;
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

.synonym-hotspot {
  top: 3%;
  left: 40%;
  width: 23%;
  height: 23%;
}

.debate-hotspot {
  top: 32%;
  left: 27%;
  width: 40%;
  height: 51%;
}

.phoenetics-hotspot {
  top: 13%;
  left: 5%;
  width: 26%;
  height: 26%;
}
</style>