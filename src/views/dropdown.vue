<template>
  <div class="dropdown-container">
    <button @click="toggle = !toggle" class="menu-button">☰ Menu</button>
    <div v-if="toggle" class="menu-items">
      <router-link to="/read">ASSESS</router-link>
      <router-link to="/improve">IMPROVE</router-link>
      <router-link to="/engage">ENGAGE</router-link>
      
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const toggle = ref(false)
</script>

<style scoped>
.dropdown-container {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 999;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.menu-button {
  background-color: #d49d3d;
  /* background-color: #455540; */
  /* color: #ccc; */
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
}

.menu-items {
  margin-top: 8px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.menu-items a {
  display: block;
  padding: 6px 12px;
  text-decoration: none;
  color: black;
}
.menu-items a:hover {
  background-color: #eee;
}
</style>