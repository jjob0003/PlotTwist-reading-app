<template>

<div class="display-word" v-if="currentWord && !gameOver">
      <div class="quiz-container">
        <img src="/phonetics.png" alt="phonetics chart" class="phonetics-img"/>
        <p>(English Club, n.d.)</p>
        <h1 class="title">📋 Phonetics Quiz</h1>
        <h2 class="subtitle">Choose the correct word for the phonetic:</h2>
        <h1>{{ currentWord.phonetics }}</h1>
      </div>

      <div class="word-grid">
        <div v-for="option in currentOptions" :key="option" class="word-card" 
            :class="{green: displayCorrectAnswer && option == currentWord.word, red: displayCorrectAnswer && option == selectedOption && option != currentWord.word}"
            @click="selectOption(option)">
            {{ option }}
        </div>
       </div>

       <button class="action-btn" @click="nextQuestion" :disabled="!displayCorrectAnswer">
        {{ nextQuestionButton() }}
       </button>
</div>

<div v-else class="quiz-container-2">
    <h1>Results</h1>
    <h2>Your final score is: {{ scoreCount }}/10</h2>
    <button class="action-btn" @click="restartQuiz">Try Again</button>
</div>
    
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const allWordsWithPhoenetics = ref([])
const allWords = ref([])
const currentWord = ref(null)
const currentOptions = ref([])


const currentIndex = ref(0)
const selectedOption = ref('')
const scoreCount = ref(0)

const displayCorrectAnswer = ref(false)
const gameOver = ref(false)

const getWordList = async () => {
    const response = await axios.get('https://reading-t9nr.onrender.com/api/words1')
    allWords.value = response.data
    allWordsWithPhoenetics.value = response.data.sort(() => 0.5 - Math.random()).slice(0,10)

    setCurrentWord()
}

onMounted( () => {
    getWordList()
})

const setCurrentWord = () => {
    currentWord.value = allWordsWithPhoenetics.value[currentIndex.value]
    currentOptions.value = displayCurrentOptions(currentWord.value.word)
}

const displayCurrentOptions = (correctAnswer) => {

    const firstLetter = correctAnswer[0]
    const secondLetter = correctAnswer[1]
    const thirdLetter = correctAnswer[2]

    const wrongOptions = allWords.value
    .filter(item => item.word != correctAnswer)
    .filter(item => item.word.length > 3)
    .filter(item => item.word[0] == firstLetter)
    .filter(item => item.word[1] == secondLetter)
    .filter(item => item.word[2] == thirdLetter)
    .map(item => item.word)
    .sort(() => 0.5 - Math.random())
    .slice(0,3)

    if(wrongOptions.length < 3){
        const extraWords = allWords.value
            .filter(item => item.word != correctAnswer)
            .map(item => item.word)
            .sort(() => 0.5 - Math.random())
            .slice(0,3 - wrongOptions.length)

        wrongOptions.push(...extraWords)

    }

    wrongOptions.push(correctAnswer)

    return wrongOptions.sort(() => 0.5 - Math.random())
}

const selectOption = (option) => {
    if(displayCorrectAnswer.value){
        return
    } else{
        selectedOption.value = option
        displayCorrectAnswer.value = true

        if(option == currentWord.value.word){
            scoreCount.value++
        }
    }
}

const nextQuestionButton = () => {
    if (currentIndex.value < allWordsWithPhoenetics.value.length - 1){
        return 'Next Question ->'
    } else{
        return 'Show results!'
    }
}

const nextQuestion = () => {
    if(currentIndex.value < allWordsWithPhoenetics.value.length - 1){
        currentIndex.value++
        selectOption.value = ''
        displayCorrectAnswer.value = false
        setCurrentWord()
    } else{
        gameOver.value = true
    }
}

const restartQuiz = () => {
    currentIndex.value = 0
    selectedOption.value = ''
    scoreCount.value = 0
    displayCorrectAnswer.value = false
    gameOver.value = false

    getWordList()
}


</script>


<style scoped>

.display-word {
    min-height: 100vh;
    background: linear-gradient(to bottom, #fff5e6, #ffd9ec);
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Baloo 2', 'Fredoka', sans-serif;
    padding: 2rem;
    flex-direction: column;
  }

  .quiz-container {
    background-color: #fffdf5;
    max-width: 800px;
    width: 100%;
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  }

  .quiz-container-2 {
    background-color: #fffdf5;
    max-width: 800px;
    width: 100%;
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: auto;
  }

  .title {
    font-size: 2.2rem;
    color: #6a4c93;
    margin-bottom: 0.3rem;
  }
  
  .subtitle {
    font-size: 1.2rem;
    color: #555;
    margin-bottom: 1.5rem;
  }

  .word-grid {
    display: flex;
    gap: 3rem;
    justify-content: center;
    margin-top: 5%;
  }
  
  .word-card {
    background-color: #ffe8f0;
    padding: 1rem;
    border-radius: 12px;
    transition: 0.2s ease;
    width: 140px;
    text-align: center;
  }

  .action-btn {
    background-color: #ffd972;
    color: #333;
    font-weight: bold;
    padding: 0.8rem 2rem;
    border: none;
    border-radius: 20px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: 0.3s ease;
    margin-top: 5%;
  }

  .green {
    background-color: rgb(157, 211, 157);
  }

  .red {
    background-color: rgb(254, 161, 161);
  }

  .phonetics-img{
    border-radius: 12px;
    margin-bottom: 3px;
    max-width: 60%;
    max-height: auto;
  }



</style>