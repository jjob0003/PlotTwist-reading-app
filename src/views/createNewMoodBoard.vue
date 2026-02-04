<template>
  <div class="background col-md-12 text-center">
    <!-- Header -->
    <div class="header col-md-12">
      <h1 class="text-header">Moodboards</h1>
    </div>

    <div class="row">
      <!-- Toolbar with image/text actions -->
      <div class="toolbar col-md-1 mt-5">
        <!-- Hidden file input for image upload -->
        <input type="file" accept="image" @change="handleImageUpload" ref="fileInput" style="display: none;" />

        <!-- Add text button -->
        <button class="button1" style="margin-top: 15%;" @click="addQuotes">
          <img src="/note.png" style="width: 30px; height:30px;" />
          <p>Add Text</p>
        </button>

        <!-- Add image via link -->
        <button class="button1" @click="addImageLink">
          <img src="/link.png" style="width: 30px; height:30px;" />
          <p>Image link</p>
        </button>

        <!-- Upload image from device -->
        <button class="button1" @click="uploadOwnImage">
          <img src="/picture.png" style="width: 30px; height:30px;" />
          <p>Upload Image</p>
        </button>

        <!-- Save moodboard as PDF -->
        <button class="button1" style="background-color: gray; color: aliceblue;" @click="saveFile">
          <img src="/save.png" style="width: 28px; height:28px;" />
          <p>Save as PDF</p>
        </button>
      </div>

      <!-- Moodboard content area -->
      <div class="container-fluid body col-md-11 mt-5" ref="exportBoard">
        <div class="itemWrap">
          <div
            v-for="(each, index) in allUploadedItems"
            :key="each.id"
            class="eachItem"
            :style="{ top: each.y + 'px', left: each.x + 'px'}"
            @mousedown.prevent="startDrag($event, index)"
            @click.stop="selectedItem = each.id"
          >
            <!-- Render text or image -->
            <div v-if="each.type == 'text'">{{ each.content }}</div>
            <div v-else-if="each.type == 'image'">
              <img :src="each.content" />
            </div>

            <!-- Delete button appears if item is selected -->
            <button v-if="selectedItem == each.id" @click="deleteItem(each.id)" class="delete-item">x</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal for adding quote text -->
  <div class="modal" v-if="displayTextModal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Add a quote from the book here:</h5>
        </div>
        <div class="modal-body">
          <input v-model="textQuote" placeholder="Enter quote" class="col-md-12" />
        </div>
        <div class="modal-footer">
          <button @click="submitQuote" class="button2">Add</button>
          <button @click="closeTextModal" class="button2">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal for adding image via URL -->
  <div class="modal" v-if="displayImageModal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Paste the image URL here:</h5>
        </div>
        <div class="modal-body">
          <input v-model="imageUrl" placeholder="Enter image link" class="col-md-12" />
        </div>
        <div class="modal-footer">
          <button @click="submitImage" class="button2">Add</button>
          <button @click="closeImageModal" class="button2">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import html2pdf from 'html2pdf.js'

// Get route ID for loading a specific moodboard
const route = useRoute()
const moodBoardID = parseInt(route.params.id)

// Main data states
const allUploadedItems = ref([])
const selectedItem = ref(null)
const displayTextModal = ref(false)
const displayImageModal = ref(false)
const textQuote = ref("")
const imageUrl = ref("")
const fileInput = ref(null)
const exportBoard = ref(null)

// Load moodboard from localStorage
const allMoodBoards = JSON.parse(localStorage.getItem('moodboards'))
const currentMoodBoard = allMoodBoards.find(mb => mb.id == moodBoardID)
allUploadedItems.value = currentMoodBoard?.items

// Auto-save when items change
watch(allUploadedItems, (newData) => {
  if (currentMoodBoard) {
    currentMoodBoard.items = newData
    localStorage.setItem('moodboards', JSON.stringify(allMoodBoards))
  }
}, { deep: true })

// Add quote modal
const addQuotes = () => displayTextModal.value = true
const closeTextModal = () => {
  textQuote.value = ""
  displayTextModal.value = false
}
const submitQuote = () => {
  if (textQuote.value) {
    allUploadedItems.value.push({ id: Date.now(), type: 'text', content: textQuote.value, x: 100, y: 100 })
  }
  closeTextModal()
}

// Add image via URL modal
const addImageLink = () => displayImageModal.value = true
const closeImageModal = () => {
  imageUrl.value = ""
  displayImageModal.value = false
}
const submitImage = () => {
  if (imageUrl.value) {
    allUploadedItems.value.push({ id: Date.now(), type: 'image', content: imageUrl.value, x: 100, y: 100 })
  }
  closeImageModal()
}

// Upload image from device
const uploadOwnImage = () => fileInput.value?.click()
const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    allUploadedItems.value.push({ id: Date.now(), type: 'image', content: reader.result, x: 100, y: 100 })
  }
  reader.readAsDataURL(file)
}

// Drag & drop logic
let indexPosition = null
let offsetX = 0
let offsetY = 0

const startDrag = (e, index) => {
  indexPosition = index
  offsetX = e.clientX - allUploadedItems.value[index].x
  offsetY = e.clientY - allUploadedItems.value[index].y
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
}

const onDrag = (e) => {
  if (indexPosition == null) return
  allUploadedItems.value[indexPosition].x = e.clientX - offsetX
  allUploadedItems.value[indexPosition].y = e.clientY - offsetY
}

const stopDrag = () => {
  indexPosition = null
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}

// Clear selected item when clicking outside
onMounted(() => {
  document.addEventListener("click", clearItemSelection)
})
const clearItemSelection = () => selectedItem.value = null

// Delete selected item
const deleteItem = (id) => {
  const confirmChoice = confirm("Are you sure you want to delete this item?")
  if (confirmChoice) {
    allUploadedItems.value = allUploadedItems.value.filter(item => item.id != id)
    selectedItem.value = null
  }
}

// Save moodboard as PDF using html2pdf
const saveFile = () => {
  if (!exportBoard.value) return
  html2pdf()
    .set({
      filename: 'mymoodboard.pdf',
      image: { type: 'jpeg', quality: 0.95 },
      html2canvas: { scale: 2, useCORS: true },
      jsPDF: { unit: 'in', format: 'a4', orientation: 'landscape' }
    })
    .from(exportBoard.value)
    .save()
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
        min-height: 650px;
        display: flex;
        flex-wrap: wrap;
        gap: 30px;
        border-radius: 10px;
        border: 8px burlywood;
        border-style:double;
        width: 1120px;
    }
     
    .toolbar{
        width: 100px;
        gap: 10px;
        background-color: rgb(242, 223, 202);
        /* background-color: rgb(195, 186, 185); */
        padding: 10px;
        display: flex;
        flex-direction: column;
        border-radius: 10px;
    }
     
    .button1{
        background-color:burlywood;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        font-size: small;
        border-color: transparent;
        border-radius: 8%;
        height: 80px;
        width: auto;
    }
     
    .button1:hover{
        background-color:antiquewhite;
        font-size: 14px;
    }
     
    .eachItem{
        background-color: transparent;
        position: absolute;
        cursor: move;
    }
     
    .delete-item{
        border: 1px solid burlywood;
        border-radius: 55%;
    }
     
    .itemWrap{
        position: relative;
        overflow: hidden;
        width: 100%;
        height: 650px;
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
        width: 500px;
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
     
    </style>