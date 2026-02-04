<template>
   <BackHomeButton />
  <router-view />
  <SpiderHelper />
  <Dropdown />
  <chatbot />
</template>

<script setup>
import BackHomeButton from './views/buttonHome.vue'
import Dropdown from './views/dropdown.vue';
import SpiderHelper from './views/spider.vue'
import chatbot from './views/chatbot.vue'
</script>
