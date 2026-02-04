<template>
  <div class="background col-md-12 text-center">
    <!-- Page Header -->
    <div class="header col-md-12">
      <h1 class="text-header">Moodboards</h1>
    </div>

    <!-- Moodboard grid section -->
    <div class="container-fluid body col-md-10 offset-md-1 mt-5">
      
      <!-- Existing moodboard tiles -->
      <div
        v-for="(each, index) in moodBoardProjects"
        :key="index"
        class="wrapper-tile"
      >
        <div class="wrap-tile">
          <!-- Clickable tile linking to the moodboard page -->
          <router-link class="tile" :to="`/moodBoard/${each.id}`"></router-link>
          <!-- Delete button -->
          <button class="delete" @click="deleteMoodBoard(each.id)">x</button>
        </div>

        <!-- Moodboard title and description -->
        <div>
          <p class="project-title" style="margin-bottom: 0;">{{ each.bookTitle }}</p>
          <p class="project-desc" style="color:rgb(195, 186, 185); margin-top: 0;">
            {{ each.bookDesc }}
          </p>
        </div>
      </div>

      <!-- "Create new moodboard" tile -->
      <div class="tile create-tile" @click="displayModal = true">+</div>
    </div>

    <!-- Modal for creating new moodboard -->
    <div class="modal" v-if="displayModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create New Project</h5>
          </div>
          <div class="modal-body">
            <input v-model="title" placeholder="Enter a book title" class="col-md-12" />
            <input v-model="description" placeholder="Enter description" class="col-md-12" style="margin-top: 5%;" />
          </div>
          <div class="modal-footer">
            <button @click="createNewMoodBoard" class="button2">Create</button>
            <button @click="closeModal" class="button2">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// Router instance
const router = useRouter()

// Modal state and form inputs
const displayModal = ref(false)
const title = ref("")
const description = ref("")

// Close modal and reset inputs
const closeModal = () => {
  displayModal.value = false
  title.value = ""
  description.value = ""
}

// Save moodboards to localStorage
const saveMoodBoard = (allMoodBoards) => {
  localStorage.setItem('moodboards', JSON.stringify(allMoodBoards))
}

// Load moodboards from localStorage
const showMoodBoards = () => {
  const dataSet = localStorage.getItem('moodboards')
  return dataSet ? JSON.parse(dataSet) : []
}

// Reactive moodboard list
const moodBoardProjects = ref(showMoodBoards())

// Create and save a new moodboard
const createNewMoodBoard = () => {
  const createID = Date.now()
  let finalTitle = title.value
  let desc = description.value

  if (!finalTitle) finalTitle = "Untitled"
  if (!desc) {
    desc = "No description"
  } else {
    const descWords = desc.trim().split(/\s+/)
    if (descWords.length > 6) {
      desc = descWords.slice(0, 6).join(" ") + "..."
    }
  }

  const newMoodBoard = {
    id: createID,
    bookTitle: finalTitle,
    bookDesc: desc,
    items: []
  }

  const allData = showMoodBoards()
  allData.push(newMoodBoard)
  saveMoodBoard(allData)
  moodBoardProjects.value = allData

  // Redirect to the new moodboard page
  router.push(`/moodBoard/${createID}`)
  displayModal.value = false
}

// Delete a moodboard by ID
const deleteMoodBoard = (id) => {
  const confirmChoice = confirm("Are you sure you want to permanently delete this moodboard?")
  if (confirmChoice === true) {
    const updateProjects = showMoodBoards().filter(mb => mb.id != id)
    saveMoodBoard(updateProjects)
    moodBoardProjects.value = updateProjects
  }
}
</script>

    
    
    <style scoped>
    .background{
      background-color: rgb(254, 239, 224);
      min-height: 800px;
    }
    
    .header{
        background-color: rgb(252, 248, 243);
        height: 80px;
    }
    
    .text-header{
        font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        color: rgb(46,57,79);
    }
    
    .body{
        background-color: rgb(252, 248, 243);
        min-height: 600px;
        display: flex;
        flex-wrap: wrap;
        gap: 30px;
        border-radius: 10px;
    
    }
    
    .tile{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
        background-color: rgb(195, 186, 185);
        height: 100px;
        width: 100px;
        text-decoration: none;
        color: rgb(46,57,79);
        border-radius: 15%;
    }
    
    .tile:hover{
        background-color:rgb(254, 239, 224);
        font-size: 17px;
    }
    
    .project-title{
        font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        color: rgb(46,57,79);
        font-weight: 600;
        max-width: 100px;
        word-wrap: break-word;
    }
    
    .project-desc{
        font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        color: rgb(46,57,79);
        font-size: small;
        max-width: 100px;
        word-wrap: break-word;
        
    }
    
    .wrapper-tile{
        display: flex;
        flex-direction: column;
        align-items: center;
        max-width: 100px;
    }
    
    .modal{
        background-color: rgb(0, 0, 0, 0.4);
        display: flex;
        align-items: center;
    }
    
    .modal-dialog{
        padding: 12px;
        background-color: rgb(254, 239, 224);
        border-radius: 6px;
    }
    
    .modal-title{
        font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        color: rgb(46,57,79);
    }
    
    .modal-body{
        font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        color: rgb(46,57,79);
    }
    
    .modal-footer{
        font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        color: rgb(46,57,79);
    }
    
    .button2{
        border-color: transparent;
    }
    
    .delete{
        position: absolute;
        top: -3px;
        right: -9px;
        border: 1px solid burlywood;
        border-radius: 55%;
    }
    
    .wrap-tile{
        position: relative;
    }
    
    </style>