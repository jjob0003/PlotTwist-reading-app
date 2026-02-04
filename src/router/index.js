import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: () => import('../views/landing.vue')  
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/generate',
    name: 'Generate',
    component: () => import('../views/Generate.vue')  
  },
  {
    path: '/readingspeed',
    name: 'ReadingSpeed',
    component: () => import('../views/readingspeed.vue')  
  },
  {
    path: '/read',
    name: 'Read',
    component: () => import('../views/read.vue')  
  },
  {
    path: '/quiz',
    name: 'Quiz',
    component: () => import('../views/quiz.vue')  
  },
  {
    path: '/readingspeedtest',
    name: 'readingspeedtest',
    component: () => import('../views/readingspeedtest.vue')  
  },
  {
    path: '/improve',
    name: 'improve',
    component: () => import('../views/improve.vue')  
  },
  {
    path: '/SynonymGame',
    name: 'SynonymGame',
    component: () => import('../views/SynonymGame.vue')  
  },
  {
    path: '/engage',
    name: 'engage',
    component: () => import('../views/engage.vue')  
  },
  {
    path: '/readinglist',
    name: 'readinglist',
    component: () => import('../views/readinglist.vue')  
  },
  {
    path: '/sharereview',
    name: 'sharereview',
    component: () => import('../views/sharereview.vue')  
  },
  {
    path: '/reviewwall',
    name: 'reviewwall',
    component: () => import('../views/reviewwall.vue')  
  },
  {
    path: '/aidebate',
    name: 'aidebate',
    component: () => import('../views/aidebate.vue')  
  },
  {
    path: '/readingstatus',
    name: 'readingstatus',
    component: () => import('../views/readingstatus.vue')  
  },
  {
    path: '/MoodBoardHome',
    name: 'MoodBoardHome',
    component: () => import('../views/MoodBoardHome.vue')  
  },
  {
    path: '/moodBoard/:id',
    name: 'createNewMoodBoard',
    component: () => import('../views/createNewMoodBoard.vue')
  },
  {
    path: '/result',
    name: 'result',
    component: () => import('../views/result.vue')
  },
  {
    path: '/chatbot',
    name: 'chatbot',
    component: () => import('../views/chatbot.vue')
  },
  {
    path: '/phoeneticsQuiz',
    name: 'phoeneticsQuiz',
    component: () => import('../views/phoeneticsQuiz.vue')
  }
]

const router = createRouter({
  history: createWebHistory('./'),
  routes
})

export default router

